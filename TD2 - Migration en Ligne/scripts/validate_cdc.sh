#!/usr/bin/env bash
set -euo pipefail

echo "[Check] Services up?"
docker ps --format '{{.Names}}' | grep -E 'gt_mysql|gt_postgres|gt_app_cdc|gt_app_faker' >/dev/null

echo "[MySQL] max(id)"
MYSQL_MAX=$(docker exec -i gt_mysql mysql -N -s -ugt_user -pgt_pass globetrotter -e "SELECT MAX(id) FROM bookings;")
echo "mysql_max_id=$MYSQL_MAX"

echo "[PostgreSQL] max(id)"
PG_MAX=$(docker exec -i gt_postgres psql -U gt_user -d globetrotter -t -A -c "SELECT MAX(id) FROM bookings;")
echo "pg_max_id=$PG_MAX"

echo "[Marker] insert 1 row in MySQL"
NEWID=$(docker exec -i gt_mysql mysql -N -s -ugt_user -pgt_pass globetrotter -e "
INSERT INTO bookings (customer_email, destination, departure_date, return_date, status)
VALUES ('test-cdc@local', CONCAT('CDC_MARK_', UNIX_TIMESTAMP()), '2026-03-01', '2026-03-10', 'CONFIRMED');
SELECT LAST_INSERT_ID();
")
echo "new_id=$NEWID"

echo "[Wait] 10s for CDC"
sleep 10

echo "[PostgreSQL] verify row replicated"
docker exec -i gt_postgres psql -U gt_user -d globetrotter -t -A -c "SELECT COUNT(*) FROM bookings WHERE id=$NEWID;"
