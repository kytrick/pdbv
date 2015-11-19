#!/bin/bash

DUMP=www.peeringdb.com/dbexport/peeringdb.sql

curl -o peeringdb.sql.new $DUMP && mv peeringdb.sql.new peeringdb.sql


