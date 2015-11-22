#!/bin/bash

# pdbv/.ebextentions/00.prime_db.config runs this script at its
# special point in the orchestration which is after the code is extracted and 
# the container is set up but before the app is deployed

cd $(dirname $0)

if ( ! mysql -u $RDS_USERNAME -p${RDS_PASSWORD} -h $RDS_HOSTNAME peeringdb -e 'show tables' ); then
  echo priming rds
  if [ ! -f peeringdb.sql ]; then
    ./fetchdb.sh
  fi
  mysql -u $RDS_USERNAME -p${RDS_PASSWORD} -h $RDS_HOSTNAME -e 'create database peeringdb'
  mysql -u $RDS_USERNAME -p${RDS_PASSWORD} -h $RDS_HOSTNAME peeringdb < peeringdb.sql
fi
