#!/usr/bin/env bash

while ! cqlsh -e 'describe cluster' ; do
    sleep 1
done
cqlsh -f setup.cql
