#!/bin/bash

cd $(dirname $0)

if ( ! mysql -u $RDS_USERNAME -p${RDS_PASSWORD} -h $RDS_HOSTNAME peeringdb -e 'show tables' ); then
  echo priming rds
  if [ ! -f peeringdb.sql ]; then
    ./fetchdb.sh
  fi
  mysql -u $RDS_USERNAME -p${RDS_PASSWORD} -h $RDS_HOSTNAME -e 'create database peeringdb'
  mysql -u $RDS_USERNAME -p${RDS_PASSWORD} -h $RDS_HOSTNAME peeringdb < peeringdb.sql
fi
