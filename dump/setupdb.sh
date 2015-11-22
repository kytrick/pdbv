#!/bin/bash

# refreshes the working copy of the database 

DB=peeringdb
brew install mysql
cd $(dirname $0)
if [ ! -f peeringdb.sql ]; then
  ./fetchdb.sh
fi

mysql -u root -e "drop database if exists $DB"
mysql -u root -e "create database $DB"
mysql -u root $DB < peeringdb.sql
