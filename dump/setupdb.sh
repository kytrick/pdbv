#!/bin/bash
DB=peeringdb
brew install mysql
mysql -u root -e "drop database if exists $DB"
mysql -u root -e "create database $DB"
mysql -u root $DB < peeringdb.sql
