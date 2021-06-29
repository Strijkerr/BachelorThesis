#!/bin/sh
# Telt het aantal files in een map
ls -I '..' -I '.' -f $1 | wc -l
