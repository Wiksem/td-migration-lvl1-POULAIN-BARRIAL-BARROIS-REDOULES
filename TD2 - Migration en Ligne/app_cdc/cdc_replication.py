import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import mysql.connector
from mysql.connector import Error as MySQLError

import psycopg2
from psycopg2 import Error as PgError


MYSQL_HOST = "gt_mysql"
MYSQL_DB = "globetrotter"
MYSQL_USER = "gt_user"
MYSQL_PASS = "gt_pass"

PG_HOST = "gt_postgres"
PG_DB = "globetrotter"
PG_USER = "gt_user"
PG_PASS = "gt_pass"

POLL_SECONDS = 2
BATCH_SIZE = 1000

STATE_FILE = "/app/cdc_state.json"


def log(msg: str) -> None:
    print(msg, flush=True)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "last_id": 0,
            "last_upd_ts": (now_utc() - timedelta(hours=2)).isoformat(),
            "last_upd_id": 0,
        }
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            s = json.load(f)
        return {
            "last_id": int(s.get("last_id", 0)),
            "last_upd_ts": s.get("last_upd_ts", (now_utc() - timedelta(hours=2)).isoformat()),
            "last_upd_id": int(s.get("last_upd_id", 0)),
        }
    except Exception:
        return {
            "last_id": 0,
            "last_upd_ts": (now_utc() - timedelta(hours=2)).isoformat(),
            "last_upd_id": 0,
        }


def save_state(state: dict) -> None:
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f)
    os.replace(tmp, STATE_FILE)


def get_mysql():
    while True:
        try:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASS,
                database=MYSQL_DB,
                autocommit=True,            # IMPORTANT: éviter transaction longue côté CDC
                connection_timeout=30,
                pool_reset_session=True,
                read_timeout=30,            # IMPORTANT: éviter un SELECT bloqué indéfiniment
                write_timeout=30,
            )
            cur = conn.cursor(dictionary=True)

            # MySQL TIMESTAMP convertit selon time_zone => on force UTC dans la session
            cur.execute("SET time_zone = '+00:00'")

            log("MySQL connected (UTC session)")
            return conn, cur
        except MySQLError as e:
            log(f"MySQL error: {type(e).__name__} - {e} (retry 5s)")
            time.sleep(5)


def get_pg():
    while True:
        try:
            conn = psycopg2.connect(
                host=PG_HOST,
                user=PG_USER,
                password=PG_PASS,
                dbname=PG_DB,
                connect_timeout=30,
            )
            cur = conn.cursor()
            cur.execute("SET TIME ZONE 'UTC'")
            conn.commit()
            log("PostgreSQL connected (UTC session)")
            return conn, cur
        except PgError as e:
            log(f"PostgreSQL error: {type(e).__name__} - {e} (retry 5s)")
            time.sleep(5)


def upsert_rows(rows, pg_cur, pg_conn):
    for r in rows:
        pg_cur.execute(
            """
            INSERT INTO bookings (id, customer_email, destination, departure_date, return_date, status, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                customer_email = EXCLUDED.customer_email,
                destination = EXCLUDED.destination,
                departure_date = EXCLUDED.departure_date,
                return_date = EXCLUDED.return_date,
                status = EXCLUDED.status,
                updated_at = EXCLUDED.updated_at
            """,
            (
                r["id"],
                r["customer_email"],
                r["destination"],
                r["departure_date"],
                r["return_date"],
                r["status"],
                r["updated_at"],
            ),
        )
    pg_conn.commit()


def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    log("Waiting for MySQL/PostgreSQL...")
    time.sleep(8)

    state = load_state()

    mysql_conn, mysql_cur = get_mysql()
    pg_conn, pg_cur = get_pg()

    last_id = state["last_id"]

    last_upd_ts = datetime.fromisoformat(state["last_upd_ts"])
    if last_upd_ts.tzinfo is None:
        last_upd_ts = last_upd_ts.replace(tzinfo=timezone.utc)
    last_upd_id = state["last_upd_id"]

    log(f"CDC start: last_id={last_id}, last_upd_ts={last_upd_ts.isoformat()}, last_upd_id={last_upd_id}")

    iteration = 0

    while True:
        iteration += 1
        try:
            # keepalive MySQL
            try:
                mysql_conn.ping(reconnect=True, attempts=3, delay=1)
            except Exception:
                log("MySQL ping failed -> reconnect")
                try:
                    mysql_cur.close()
                    mysql_conn.close()
                except Exception:
                    pass
                mysql_conn, mysql_cur = get_mysql()

            # Défensif: si une transaction est restée ouverte, on la termine
            try:
                mysql_conn.rollback()
            except Exception:
                pass

            # 1) Replication INSERT via id
            mysql_cur.execute(
                "SELECT * FROM bookings WHERE id > %s ORDER BY id LIMIT %s",
                (last_id, BATCH_SIZE),
            )
            insert_rows = mysql_cur.fetchall()

            if insert_rows:
                upsert_rows(insert_rows, pg_cur, pg_conn)
                last_id = insert_rows[-1]["id"]

                # Avancer aussi le watermark update
                last_seen_ts = insert_rows[-1]["updated_at"]
                if last_seen_ts.tzinfo is None:
                    last_seen_ts = last_seen_ts.replace(tzinfo=timezone.utc)
                last_upd_ts = max(last_upd_ts, last_seen_ts)
                last_upd_id = max(last_upd_id, last_id)

                state["last_id"] = last_id
                state["last_upd_ts"] = last_upd_ts.isoformat()
                state["last_upd_id"] = last_upd_id
                save_state(state)

                log(f"[{now_utc().strftime('%H:%M:%SZ')}] INSERT +{len(insert_rows)} => last_id={last_id}")
                continue

            # 2) Replication UPDATE (optional) via (updated_at, id) on id <= last_id
            mysql_cur.execute(
                """
                SELECT *
                FROM bookings
                WHERE id <= %s
                  AND (
                        updated_at > %s
                     OR (updated_at = %s AND id > %s)
                  )
                ORDER BY updated_at, id
                LIMIT %s
                """,
                (
                    last_id,
                    last_upd_ts.replace(tzinfo=None),
                    last_upd_ts.replace(tzinfo=None),
                    last_upd_id,
                    BATCH_SIZE,
                ),
            )
            upd_rows = mysql_cur.fetchall()

            if upd_rows:
                upsert_rows(upd_rows, pg_cur, pg_conn)

                last_row = upd_rows[-1]
                ts = last_row["updated_at"]
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                last_upd_ts = ts
                last_upd_id = last_row["id"]

                state["last_upd_ts"] = last_upd_ts.isoformat()
                state["last_upd_id"] = last_upd_id
                save_state(state)

                log(
                    f"[{now_utc().strftime('%H:%M:%SZ')}] UPDATE +{len(upd_rows)} "
                    f"=> last_upd_ts={last_upd_ts.isoformat()} last_upd_id={last_upd_id}"
                )

            if iteration % 30 == 0:
                log(f"[{now_utc().strftime('%H:%M:%SZ')}] OK (idle) last_id={last_id}")

            time.sleep(POLL_SECONDS)

        except PgError as e:
            log(f"PostgreSQL error: {type(e).__name__} - {e} -> rollback + reconnect")
            try:
                pg_conn.rollback()
            except Exception:
                pass
            try:
                pg_cur.close()
                pg_conn.close()
            except Exception:
                pass
            pg_conn, pg_cur = get_pg()
            time.sleep(2)

        except Exception as e:
            log(f"CDC error: {type(e).__name__} - {e} (sleep 5s)")
            time.sleep(5)


if __name__ == "__main__":
    main()
