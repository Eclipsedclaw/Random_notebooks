#!/bin/zsh

. ~/.zsh_usr/zsh_script

num=1000000
energy=1000

ln -s ../../bkg/database .
ln -s ../../bkg/parfile_HY2020.json .

./run_simulation.rb ${num} ${energy} > run_simulation.log 2>&1
./extract_compton_events.rb > extract_compton_events.log 2>&1
root add_param.cpp << EOF
.q
EOF
