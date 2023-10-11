#!/usr/bin/env python
# coding: UTF-8

import sys, ROOT
import numpy as np
import pandas as pd

particle_names = ["neutro", "proton", "he---4", "muplus", "mumins", "electr", "positr", "photon"]

def make_spectrum(df, particle_name):
    energy = np.unique(df.query('particle == "{}"'.format(particle_name))["energy"].values)
    
    flux = []
    for _energy in energy:
        _flux = 0

        _df = df.query('particle == "{}" & energy == {}'.format(particle_name, _energy))
        _costheta = _df["costheta"].values
        _diff_flux = _df["flux"].values
        
        delta_costheta = 2.0/(len(_costheta) - 1)
        for i in range(len(_costheta) - 1):
            _flux += _diff_flux[i] * delta_costheta * np.pi * 2
        flux.append(_flux)

    return energy, np.array(flux)

def get_tgraph_spectrum(df, particle_name, graphname = None):
    energy, flux = make_spectrum(df, particle_name)
    tg = ROOT.TGraph(len(energy), energy, flux)
    if graphname == None:
        graphname = "spectrum_{}".format(particle_name)
    tg.SetNameTitle(graphname, graphname+";Energy (MeV);Flux (/cm2/s/MeV)")

    return tg

def make_diff_spectrum(df, particle_name, costheta):
    energy = np.unique(df.query('particle == "{}"'.format(particle_name))["energy"].values)

    _df = df.query('particle == "{}" & costheta == {}'.format(particle_name, costheta))
    
    diff_flux = []
    for _energy in energy:
        _diff_flux = _df.query("energy == {}".format(_energy))["flux"].values[0]
        diff_flux.append(_diff_flux)

    return energy, np.array(diff_flux)

def get_tgraph_diff_spectrum(df, particle_name, costheta, graphname = None):
    energy, flux = make_diff_spectrum(df, particle_name, costheta)
    tg = ROOT.TGraph(len(energy), energy, flux)
    if graphname == None:
        graphname = "spectrum_{}_costheta{}".format(particle_name, costheta)
    tg.SetNameTitle(graphname, graphname+";Energy (MeV);Flux (/cm2/s/MeV/sr)")

    return tg

def main(infilename):
    df = pd.read_csv(infilename)
    particle_names = np.unique(df["particle"].values)
    costheta = np.unique(df["costheta"].values)
   
    rootfilename = infilename.split("/")[-1].replace(".csv", ".root")
    rootfile = ROOT.TFile(rootfilename, "recreate")
    for particle in particle_names:
        print("particle = {}".format(particle))
        tg = get_tgraph_spectrum(df, particle)
        rootfile.cd()
        tg.Write()
        
        rootfile.mkdir("diff_flux_{}".format(particle))
        rootfile.cd("diff_flux_{}".format(particle))
        for _costheta in costheta:
            print("    costheta = {}".format(_costheta))
            if _costheta == 1.0:
                continue
            tg = get_tgraph_diff_spectrum(df, particle, _costheta)
            tg.Write()
    rootfile.Close()

if __name__=="__main__":
    infilename = sys.argv[1]
    main(infilename)
