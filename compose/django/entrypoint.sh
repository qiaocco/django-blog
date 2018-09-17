#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

mysql_ready() {
python << END
import sys

import pymysql

try:
    pymysql.connect(
        db="${MYSQL_DB}",
        user="${MYSQL_USER}",
        password="${MYSQL_PASSWORD}",
        host="${MYSQL_HOST}",
    )
except pymysql.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
until mysql_ready; do
  >&2 echo 'Waitings for MySQL to become available...'
  sleep 1
done
>&2 echo 'MySQL is available'

exec "$@"
