#!/usr/bin/env python
# coding: UTF-8

import sys
import ROOT
import numpy as np
import json

segment = 2

outfilename_csv = "sensitivity_segment{}.csv".format(segment)
outfilename_root = "sensitivity_segment{}.root".format(segment)

T_obs = 3024000.0 #35 days

Asim_source = np.pi * 110 ** 2
Nsim_source = 10000000
Emin_source = 0.5 #MeV
Emax_source = 15.0 #MeV
powerlawindex_source = 2.0

Asim_bkg = np.pi * 110 ** 2
T_bkg = 608.101 

list_energy_center = [ 0.7, 1, 2, 4, 6 ] #MeV
delta_energy_ratio = 0.5

MeVtoErg = 1.602176565e-06
sigma = 3

def main():
    csvfile = open(outfilename_csv, "w")
    csvfile.write("energy_center,vFv_sensitivity_at_energy_center,Ndet_bkg,Ndet_source\n")
    
    list_sensitivity_at_energy_center = []

    for energy_center in list_energy_center:
        with open("ana_bkg_segment{}_E{}.json".format(segment, energy_center), "r") as f:
            jsonfile_bkg = json.load(f)
            Ndet_bkg = jsonfile_bkg['Ndet']

        with open("ana_source_segment{}_E{}.json".format(segment, energy_center), "r") as f:
            jsonfile_source = json.load(f)
            Ndet_source = jsonfile_source['Ndet']

        ### reference flux calculation ###
        norm_all = energy_center / (1-powerlawindex_source) * ( (Emax_source/energy_center)**(1-powerlawindex_source) - (Emin_source/energy_center)**(1-powerlawindex_source) )
        diffflux_at_energy_center_ref = Nsim_source / Asim_source / T_bkg / norm_all #ph/cm2/s/MeV

        ### 3sigma flux ###
        sensitivity_at_energy_center = diffflux_at_energy_center_ref / Ndet_source * (T_obs/T_bkg)**-0.5 * sigma * (Ndet_bkg)**0.5
        vFv_sensitivity_at_energy_center = sensitivity_at_energy_center * energy_center**2 * MeVtoErg

        print(energy_center, vFv_sensitivity_at_energy_center, Ndet_bkg, Ndet_source)
        csvfile.write("{},{},{},{}\n".format(energy_center, vFv_sensitivity_at_energy_center, Ndet_bkg, Ndet_source))

        list_sensitivity_at_energy_center.append(vFv_sensitivity_at_energy_center)

    rootfile = ROOT.TFile(outfilename_root, "recreate")
    tg_sensitivity = ROOT.TGraph(len(list_energy_center), np.array(list_energy_center), np.array(list_sensitivity_at_energy_center))
    tg_sensitivity.SetNameTitle("vFv_sensitivity", "vFv_sensitivity;Energy (MeV);Continuum sensivitity (erg cm-2 s-1)")
    rootfile.cd()
    tg_sensitivity.Write()
    rootfile.Close()

if __name__=="__main__":
    main()

