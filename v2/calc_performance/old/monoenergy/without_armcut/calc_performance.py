#!/usr/bin/env python
# coding: UTF-8

import sys
import json
import ROOT
import numpy as np

#parfilenames = [ "E_250.json", "E_500.json", "E_750.json", "E_1000.json", "E_2000.json", "E_4000.json", "E_8000.json", "E_16000.json" ]
parfilenames = [ "E_500.json", "E_750.json", "E_1000.json", "E_2000.json", "E_4000.json", "E_8000.json" ]
outfilename = "performance_without_armcut.root"

def main(parfilenames, outfilename):
    ene = []
    Aeff = []
    ARM_FWHM = []
    energy_FWHM = []

    for parfilename in parfilenames:
        with open(parfilename) as f:
            parfile = json.load(f)
        ene.append(parfile["ini_energy"])
        Aeff.append(parfile["Aeff"])
        ARM_FWHM.append(parfile["ARM_FWHM"])
        energy_FWHM.append(parfile["energy_FWHM"])

    outfile = ROOT.TFile(outfilename, "recreate")

    tg_Aeff = ROOT.TGraph(len(ene), np.array(ene), np.array(Aeff))
    tg_Aeff.SetNameTitle("tg_Aeff", "tg_Aeff;Energy (keV);Aeff (cm2)")
    tg_ARM_FWHM = ROOT.TGraph(len(ene), np.array(ene), np.array(ARM_FWHM))
    tg_ARM_FWHM.SetNameTitle("tg_ARM_FWHM", "tg_ARM_FWHM;Energy (keV);ARM FHWM(deg.)")
    tg_energy_FWHM = ROOT.TGraph(len(ene), np.array(ene), np.array(energy_FWHM) / np.array(ene) * 100)
    tg_energy_FWHM.SetNameTitle("tg_energy_FWHM", "tg_energy_FWHM;Energy (keV);Energy Resolution FHWM (%)")

    outfile.cd()
    tg_Aeff.Write()
    tg_ARM_FWHM.Write()
    tg_energy_FWHM.Write()
    outfile.Close()

if __name__=="__main__":
    main(parfilenames, outfilename)
