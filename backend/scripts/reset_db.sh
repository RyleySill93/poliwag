#!/bin/sh

dropdb -U poliwag poliwag
createdb -O poliwag -E UTF8 -T template1 poliwag
