#!/bin/bash
shopt -s expand_aliases

cd scripts
source virtualEnv.sh

curr_addr=$(pwd)/channel_dispatcher.py
alias channel_dispatcher='python '$curr_addr