#!/bin/bash

brew install mysql
echo 'create database peeringdb' | mysql -u root
mysql -u root peeringdb < peeringdb.sql
