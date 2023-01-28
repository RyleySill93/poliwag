#!/bin/sh

psql -d postgres -c "create role poliwag login password 'dev1';"
psql -d postgres -c "ALTER USER poliwag WITH SUPERUSER;"
createdb -O poliwag -E UTF8 -T template1 poliwag
