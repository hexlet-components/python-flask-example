#!/bin/bash

set -m

/usr/lib/postgresql/15/bin/postgres \
    -D /var/lib/postgresql/15/main \
    -c config_file=/etc/postgresql/15/main/postgresql.conf &

sleep 5 && psql -a -f init.sql && make run

fg %1
