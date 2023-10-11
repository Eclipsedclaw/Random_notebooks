#!/bin/zsh

. ~/.zsh_usr/zsh_script

./run_simulation.rb > run_simulation.log 2>&1
./extract_compton_events.rb > extract_compton_events.log 2>&1
root add_param.cpp << EOF
.q
EOF
