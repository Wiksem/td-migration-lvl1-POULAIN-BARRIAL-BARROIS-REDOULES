#!/usr/bin/env bash
set -euo pipefail

echo "[MySQL] volume + confirmed"
docker exec -it gt_mysql mysql -ugt_user -pgt_pass globetrotter -e "
SELECT COUNT(*) AS mysql_count FROM bookings;
SELECT status, COUNT(*) AS n FROM bookings GROUP BY status ORDER BY status;
"

echo "[PostgreSQL] volume + confirmed"
docker exec -it gt_postgres psql -U gt_user -d globetrotter -c "
SELECT COUNT(*) AS pg_count FROM bookings;
SELECT status, COUNT(*) AS n FROM bookings GROUP BY status ORDER BY status;
"
