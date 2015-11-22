#!/bin/bash

# gets a fresh copy of the peeringdb nightly dump

DUMP=www.peeringdb.com/dbexport/peeringdb.sql

# peeringdb threatens to make their mysql dump go away.
# this makes sure we'll always have the last legacy copy

curl -o peeringdb.sql.new $DUMP && mv peeringdb.sql.new peeringdb.sql


