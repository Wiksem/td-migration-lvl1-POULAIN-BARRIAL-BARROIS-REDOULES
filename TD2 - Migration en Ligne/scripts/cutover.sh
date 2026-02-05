#!/usr/bin/env bash
set -euo pipefail

echo "[Cutover] 1) Stop writes on MySQL (stop faker)"
docker compose stop app_faker

echo "[Cutover] 2) Wait until CDC catches up (max(id) equal)"
for i in $(seq 1 60); do
  MYSQL_MAX=$(docker exec -i gt_mysql mysql -N -s -ugt_user -pgt_pass globetrotter -e "SELECT COALESCE(MAX(id),0) FROM bookings;")
  PG_MAX=$(docker exec -i gt_postgres psql -U gt_user -d globetrotter -t -A -c "SELECT COALESCE(MAX(id),0) FROM bookings;")

  echo "Try $i/60 : mysql_max_id=$MYSQL_MAX pg_max_id=$PG_MAX"

  if [ "$MYSQL_MAX" = "$PG_MAX" ]; then
    echo "[Cutover] OK: CDC caught up"
    break
  fi

  sleep 2
done

echo "[Cutover] 3) Business validation"
./scripts/validate_business.sh

echo "[Cutover] Done. You can now switch application DB endpoint to PostgreSQL."
