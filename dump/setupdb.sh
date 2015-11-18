#!/bin/bash
DB=peeringdb
brew install mysql
mysql -u root -e "drop database if exists $DB"
mysql -u root -e "create database $DB"
mysql -u root $DB < peeringdb.sql
cat <<EOF | mysql -u root $DB
update MgmtPublics set region_continent = "Asia Pacific" where country like "RU";
update MgmtPublics set region_continent = "South America" where country like "BR";
update MgmtPublics set region_continent = "Asia Pacific" where country like "NZ";
update MgmtPublics set region_continent = "South America" where country like "PE";
update MgmtPublics set region_continent = "North America" where country like "US";
EOF
