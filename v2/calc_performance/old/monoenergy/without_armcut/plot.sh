#!/bin/zsh

. ~/.zsh_usr/zsh_script

for file in E*root
do
    python ./plot.py $file
done
