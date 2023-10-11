#!/bin/zsh

. ~/.zsh_usr/zsh_script

segment=2

ln -s ../../simulation/source_powerlaw/cetree_source_addparam.root
ln -s ../../simulation/bkg/cetree_bkg_addparam.root
ln -s ../script/ana.py
ln -s ../script/calFWHM.py

for E in 0.7 1 2 4 6
do
python ana.py cetree_source_addparam.root ana_source_segment${segment}_E${E}.root parfile_cut1_segment${segment}_armfunccut_E${E}MeV.json 10000
python ana.py cetree_bkg_addparam.root ana_bkg_segment${segment}_E${E}.root parfile_cut1_segment${segment}_armfunccut_E${E}MeV.json 10000
done
