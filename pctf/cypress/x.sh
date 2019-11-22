#!/bin/bash

export LD_LIBRARY_PATH=".:$LD_LIBRARY_PATH"

set -ex

./splaid-cypress -h
./splaid-cypress -%c
