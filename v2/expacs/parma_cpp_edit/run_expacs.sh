#!/bin/zsh

. ~/.zsh_usr/zsh_script

g++ main.cpp subroutines.cpp -o expacs_w_csvfile

for file in AliceSprings_Australia_2021_3_21_alt30000m EsrangeKiruna_Sweden_2021_3_21_alt30000m FortSumner_NewMexico_2021_3_21_alt30000m McMurdoStation_Antarctica_2021_3_21_alt30000m PacificMissileRangeFacility_Hawaii_2021_3_21_alt30000m Palestine_Texas_2021_3_21_alt30000m Taikichou_Japan_2021_3_21_alt30000m Wanaka_NewZealand_2021_3_21_alt30000m
do
./expacs_w_csvfile $file
done
