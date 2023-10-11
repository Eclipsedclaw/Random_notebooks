#!/bin/zsh

. ~/.zsh_usr/zsh_script

parfile=parfile_cut1_segment2_armfunccut.json

ln -s ../../script/ana.py .
ln -s ../../script/calFWHM.py .

for E in 250 500 750 1000 2000 4000 8000 16000
do
python ana.py ../../../simulation/source_monoenergy/E_${E}/cetree_source_monoenergy_addparam.root E_${E}.root ${parfile} ${E}
done
