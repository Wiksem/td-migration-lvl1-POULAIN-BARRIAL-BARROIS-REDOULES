#!/usr/bin/env bash
set -euo pipefail

echo "[MySQL] COUNT(*) / MAX(id)"
docker exec -i gt_mysql mysql -N -s -ugt_user -pgt_pass globetrotter \
  -e "SELECT COUNT(*) AS mysql_count, MAX(id) AS mysql_max_id FROM bookings;"

echo "[PostgreSQL] COUNT(*) / MAX(id)"
docker exec -i gt_postgres psql -U gt_user -d globetrotter -t -A \
  -c "SELECT COUNT(*) AS pg_count, MAX(id) AS pg_max_id FROM bookings;"
