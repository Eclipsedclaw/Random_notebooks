#!/bin/zsh

. ~/.zsh_usr/zsh_script

for E in 250 500 750 1000 2000 4000 8000 16000
do
rsync -av template/ E_${E}/
sed -i -e "s/energy=1000/energy=${E}/g" E_${E}/run_sim_source.sh
rm -f E_${E}/run_sim_source.sh-e
done
