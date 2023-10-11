#!/bin/zsh

. ~/.zsh_usr/zsh_script

function conv_expacsout2csv () {
infile=$1
python conv_csv.py $infile
}

function conv_csv2fits_map() {
infiledir=$1
infile=$2
particle=$3

outfile=${infile/.csv/_map_${particle}.fits}

python mk_healpix_map.py ${infiledir}/$infile ${outfile} ${particle}
}

function conv_csv2fits_PL() {
infiledir=$1
infile=$2
particle=$3

outfile=${infile/.csv/_powerlaw_${particle}.fits}

python mk_healpix_map_powerlaw.py ${infiledir}/$infile ${outfile} ${particle}
}

infiledir=../parma_cpp_edit/AngOutCsv

for infile in AliceSprings_Australia_2021_3_21_alt30000m.csv EsrangeKiruna_Sweden_2021_3_21_alt30000m.csv FortSumner_NewMexico_2021_3_21_alt30000m.csv McMurdoStation_Antarctica_2021_3_21_alt30000m.csv PacificMissileRangeFacility_Hawaii_2021_3_21_alt30000m.csv Palestine_Texas_2021_3_21_alt30000m.csv Taikichou_Japan_2021_3_21_alt30000m.csv Wanaka_NewZealand_2021_3_21_alt30000m.csv
do
#conv_expacsout2csv ${infiledir} ${infile}
conv_csv2fits_map ${infiledir} ${infile} photon
conv_csv2fits_map ${infiledir} ${infile} neutro
conv_csv2fits_PL ${infiledir} ${infile} photon
conv_csv2fits_PL ${infiledir} ${infile} neutro
done
