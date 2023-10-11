#!/usr/bin/env python
# coding: UTF-8

import sys
import json
import ROOT
import numpy as np
import calFWHM

def main(infilename, outfilename, parfilename, ini_energy):
    infile = ROOT.TFile(infilename, "r")
    cetree = infile.Get("cetree")

    outfile = ROOT.TFile(outfilename, "recreate")
    
    with open(parfilename, "r") as f:
        parfile = json.load(f)

    Nsim = parfile["Nsim"]
    Asim = parfile["Asim"]
    
    condition  = "{} <= num_hits && num_hits <= {}".format(parfile["num_hits"]["min"], 
                                                           parfile["num_hits"]["max"])
    condition += " && {} <= energy_reconstructed && energy_reconstructed <= {}".format(parfile["energy_reconstructed"]["min"], 
                                                                                   parfile["energy_reconstructed"]["max"])
    condition += " && {} <= total_energy_deposit && total_energy_deposit <= {}".format(parfile["total_energy_deposit"]["min"], 
                                                                                   parfile["total_energy_deposit"]["max"])
    condition += " && {} <= scattering_angle && scattering_angle <= {}".format(parfile["scattering_angle"]["min"] * np.pi / 180, 
                                                                               parfile["scattering_angle"]["max"] * np.pi / 180)
    condition += " && {} <= hit1_energy && hit1_energy <= {}".format(parfile["hit1_energy"]["min"],
                                                                     parfile["hit1_energy"]["max"])
    condition += " && {} <= hit2_energy && hit2_energy <= {}".format(parfile["hit2_energy"]["min"],
                                                                     parfile["hit2_energy"]["max"])
    condition += " && {} <= hit1_posx && hit1_posx <= {}".format(parfile["hit1_pos"]["x"]["min"],
                                                                 parfile["hit1_pos"]["x"]["max"])
    condition += " && {} <= hit1_posy && hit1_posy <= {}".format(parfile["hit1_pos"]["y"]["min"],
                                                                 parfile["hit1_pos"]["y"]["max"])
    condition += " && {} <= hit1_posz && hit1_posz <= {}".format(parfile["hit1_pos"]["z"]["min"],
                                                                 parfile["hit1_pos"]["z"]["max"])
    condition += " && {} <= hit2_posx && hit2_posx <= {}".format(parfile["hit2_pos"]["x"]["min"],
                                                                 parfile["hit2_pos"]["x"]["max"])
    condition += " && {} <= hit2_posy && hit2_posy <= {}".format(parfile["hit2_pos"]["y"]["min"],
                                                                 parfile["hit2_pos"]["y"]["max"])
    condition += " && {} <= hit2_posz && hit2_posz <= {}".format(parfile["hit2_pos"]["z"]["min"],
                                                                 parfile["hit2_pos"]["z"]["max"])
    condition += " && {} <= first_interaction_distance && first_interaction_distance <= {}".format(parfile["first_interaction_distance"]["min"],
                                                                                                   parfile["first_interaction_distance"]["max"])
    condition += " && {} <= reconstruction_fraction && reconstruction_fraction <= {}".format(parfile["reconstruction_fraction"]["min"],
                                                                                             parfile["reconstruction_fraction"]["max"])
    condition += " && {} <= TMath::Log(likelihood) && TMath::Log(likelihood) <= {}".format(parfile["loglikelihood"]["min"],
                                                                                           parfile["loglikelihood"]["max"])
    condition += " && {} <= dtheta && dtheta <= {}".format(parfile["ARM"]["min"] * np.pi / 180,
                                                           parfile["ARM"]["max"] * np.pi / 180)
    condition += " && segment_flag >= {}".format(parfile["segment_flag"])
    if parfile["escape_flag"] == 0:
        condition += " && escape_flag == 0"
    elif parfile["escape_flag"] == 1:
        condition += " && escape_flag == 1"

    try:
        arm_func_name = parfile["ARM"]["ARM_func"]["filename"]
        arm_sigma = parfile["ARM"]["ARM_func"]["sigma"]

        import pandas as pd
        arm_func_pars = pd.read_csv(arm_func_name)
        p0 = arm_func_pars['p0'][0]
        p1 = arm_func_pars['p1'][0]
        p2 = arm_func_pars['p2'][0]
        condition += " && TMath::Abs(dtheta * 180 / TMath::Pi()) <= ({} + TMath::Log(energy_reconstructed) * {} + TMath::Log(energy_reconstructed) * TMath::Log(energy_reconstructed) * {})/ 2.35 * {}".format(p0, p1, p2, arm_sigma)
    except:
            pass

    cetree_cutapplied = cetree.CopyTree(condition)

#1d hist
    hist_ARM = ROOT.TH1D("hist_ARM", "hist_ARM;ARM (deg.);counts", 729, -180, 180)
    cetree_cutapplied.Draw("dtheta * 180 / TMath::Pi() >> hist_ARM")

    hist_num_hits = ROOT.TH1D("hist_num_hits", "hist_num_hits;num_hits;counts", 10, 0-0.5, 10-0.5)
    cetree_cutapplied.Draw("num_hits >> hist_num_hits")

    hist_energy = ROOT.TH1D("hist_energy", "hist_energy;energy (keV);counts/5keV", 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("energy_reconstructed >> hist_energy")

    hist_total_energy_deposit = ROOT.TH1D("hist_total_energy_deposit", "hist_total_energy_deposit;total_energy_deposit (keV);counts/5keV", 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("total_energy_deposit >> hist_total_energy_deposit")

    hist_scattering_angle = ROOT.TH1D("hist_scattering_angle", "hist_scattering_angle;scattering_angle (deg.);counts", 512, 0, 180)
    cetree_cutapplied.Draw("scattering_angle * 180 / TMath::Pi() >> hist_scattering_angle")

    hist_hit1_energy = ROOT.TH1D("hist_hit1_energy", "hist_hit1_energy;hit1_energy (keV);counts", 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("hit1_energy >> hist_hit1_energy")

    hist_hit2_energy = ROOT.TH1D("hist_hit2_energy", "hist_hit2_energy;hit2_energy (keV);counts", 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("hit2_energy >> hist_hit2_energy")

    hist_hit1_posx = ROOT.TH1D("hist_hit1_posx", "hist_hit1_posx;hit1_posx (cm);counts", 2048, -140, 140)
    cetree_cutapplied.Draw("hit1_posx >> hist_hit1_posx")

    hist_hit1_posy = ROOT.TH1D("hist_hit1_posy", "hist_hit1_posy;hit1_posy (cm);counts", 2048, -140, 140)
    cetree_cutapplied.Draw("hit1_posy >> hist_hit1_posy")

    hist_hit1_posz = ROOT.TH1D("hist_hit1_posz", "hist_hit1_posz;hit1_posz (cm);counts", 2048, -140, 140)
    cetree_cutapplied.Draw("hit1_posz >> hist_hit1_posz")

    hist_hit2_posx = ROOT.TH1D("hist_hit2_posx", "hist_hit2_posx;hit2_posx (cm);counts", 2048, -140, 140)
    cetree_cutapplied.Draw("hit2_posx >> hist_hit2_posx")

    hist_hit2_posy = ROOT.TH1D("hist_hit2_posy", "hist_hit2_posy;hit2_posy (cm);counts", 2048, -140, 140)
    cetree_cutapplied.Draw("hit2_posy >> hist_hit2_posy")

    hist_hit2_posz = ROOT.TH1D("hist_hit2_posz", "hist_hit2_posz;hit2_posz (cm);counts", 2048, -140, 140)
    cetree_cutapplied.Draw("hit2_posz >> hist_hit2_posz")

    hist_first_interaction_distance = ROOT.TH1D("hist_first_interaction_distance", "hist_first_interaction_distance;first_interaction_distance (cm);counts", 1024, 0, 200)
    cetree_cutapplied.Draw("first_interaction_distance >> hist_first_interaction_distance")

    hist_reconstruction_fraction = ROOT.TH1D("hist_reconstruction_fraction", "hist_reconstruction_fraction;reconstruction_fraction;counts", 1024, 0.0, 1.0)
    cetree_cutapplied.Draw("reconstruction_fraction >> hist_reconstruction_fraction")

    hist_loglikelihood = ROOT.TH1D("hist_loglikelihood", "hist_loglikelihood;loglikelihood;counts", 2048, -100.0, 10.0)
    cetree_cutapplied.Draw("TMath::Log(likelihood) >> hist_loglikelihood")

    hist_escape_flag = ROOT.TH1D("hist_escape_flag", "hist_escape_flag;escape_flag;counts", 2, -0.5, 1.5)
    cetree_cutapplied.Draw("escape_flag >> hist_escape_flag")

    hist_segment_flag = ROOT.TH1D("hist_segment_flag", "hist_segment_flag;segment_flag;counts", 16, 0-0.5, 16-0.5)
    cetree_cutapplied.Draw("segment_flag >> hist_segment_flag")

#2d hist
    hist2d_ARM_energy_reconstructed = ROOT.TH2D("hist2d_ARM_energy_reconstructed", "hist2d_ARM_energy_reconstructed;ARM (deg.);energy_reconstructed (keV)", 729, -180, 180, 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("energy_reconstructed:dtheta * 180 / TMath::Pi() >> hist2d_ARM_energy_reconstructed")

    hist2d_ARM_total_energy_deposit = ROOT.TH2D("hist2d_ARM_total_energy_deposit", "hist2d_ARM_total_energy_deposit;ARM (deg.);total_energy_deposit (keV)", 729, -180, 180, 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("total_energy_deposit:dtheta * 180 / TMath::Pi() >> hist2d_ARM_total_energy_deposit")

    hist2d_ARM_scattering_angle = ROOT.TH2D("hist2d_ARM_scattering_angle", "hist2d_ARM_scattering_angle;ARM (deg.);scattering_angle (keV)", 729, -180, 180, 512, 0, 180)
    cetree_cutapplied.Draw("scattering_angle * 180 / TMath::Pi():dtheta * 180 / TMath::Pi() >> hist2d_ARM_scattering_angle")

    hist2d_ARM_hit1_energy = ROOT.TH2D("hist2d_ARM_hit1_energy", "hist2d_ARM_hit1_energy;ARM (deg.);hit1_energy (keV)", 729, -180, 180, 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("hit1_energy:dtheta * 180 / TMath::Pi() >> hist2d_ARM_hit1_energy")

    hist2d_ARM_hit2_energy = ROOT.TH2D("hist2d_ARM_hit2_energy", "hist2d_ARM_hit2_energy;ARM (deg.);hit2_energy (keV)", 729, -180, 180, 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("hit2_energy:dtheta * 180 / TMath::Pi() >> hist2d_ARM_hit2_energy")

    hist2d_ARM_first_interaction_distance = ROOT.TH2D("hist2d_ARM_first_interaction_distance", "hist2d_ARM_first_interaction_distance;ARM (deg.);first_interaction_distance (cm)", 729, -180, 180, 1024, 0, 200)
    cetree_cutapplied.Draw("first_interaction_distance:dtheta * 180 / TMath::Pi() >> hist2d_ARM_first_interaction_distance")

    hist2d_ARM_reconstruction_fraction = ROOT.TH2D("hist2d_ARM_reconstruction_fraction", "hist2d_ARM_reconstruction_fraction;ARM (deg.);reconstruction_fraction", 729, -180, 180, 1024, 0.0, 1.0)
    cetree_cutapplied.Draw("reconstruction_fraction:dtheta * 180 / TMath::Pi() >> hist2d_ARM_reconstruction_fraction")

    hist2d_ARM_loglikelihood = ROOT.TH2D("hist2d_ARM_loglikelihood", "hist2d_ARM_loglikelihood;ARM (deg.);loglikelihood", 729, -180, 180, 2048, -100.0, 10.0)
    cetree_cutapplied.Draw("TMath::Log(likelihood):dtheta * 180 / TMath::Pi() >> hist2d_ARM_loglikelihood")

    hist2d_energy_reconstructed_total_energy_deposit = ROOT.TH2D("hist2d_energy_reconstructed_total_energy_deposit", "hist2d_energy_reconstructed_total_energy_deposit;energy_reconstructed (keV);total_energy_deposit (keV)", 4096, 0, 4096 * 5, 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("total_energy_deposit:energy_reconstructed >> hist2d_energy_reconstructed_total_energy_deposit")

    hist2d_energy_reconstructed_scattering_angle = ROOT.TH2D("hist2d_energy_reconstructed_scattering_angle", "hist2d_energy_reconstructed_scattering_angle;energy_reconstructed (keV);scattering_angle (keV)", 4096, 0, 4096 * 5, 512, 0, 180)
    cetree_cutapplied.Draw("scattering_angle * 180 / TMath::Pi():energy_reconstructed >> hist2d_energy_reconstructed_scattering_angle")

    hist2d_energy_reconstructed_hit1_energy = ROOT.TH2D("hist2d_energy_reconstructed_hit1_energy", "hist2d_energy_reconstructed_hit1_energy;energy_reconstructed (keV);hit1_energy (keV)", 4096, 0, 4096 * 5, 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("hit1_energy:energy_reconstructed >> hist2d_energy_reconstructed_hit1_energy")

    hist2d_energy_reconstructed_hit2_energy = ROOT.TH2D("hist2d_energy_reconstructed_hit2_energy", "hist2d_energy_reconstructed_hit2_energy;energy_reconstructed (keV);hit2_energy (keV)", 4096, 0, 4096 * 5, 4096, 0, 4096 * 5)
    cetree_cutapplied.Draw("hit2_energy:energy_reconstructed >> hist2d_energy_reconstructed_hit2_energy")

    hist2d_energy_reconstructed_first_interaction_distance = ROOT.TH2D("hist2d_energy_reconstructed_first_interaction_distance", "hist2d_energy_reconstructed_first_interaction_distance;energy_reconstructed (keV);first_interaction_distance (cm)", 4096, 0, 4096 * 5, 1024, 0, 200)
    cetree_cutapplied.Draw("first_interaction_distance:energy_reconstructed >> hist2d_energy_reconstructed_first_interaction_distance")

    hist2d_energy_reconstructed_reconstruction_fraction = ROOT.TH2D("hist2d_energy_reconstructed_reconstruction_fraction", "hist2d_energy_reconstructed_reconstruction_fraction;energy_reconstructed (keV);reconstruction_fraction", 4096, 0, 4096 * 5, 1024, 0.0, 1.0)
    cetree_cutapplied.Draw("reconstruction_fraction:energy_reconstructed >> hist2d_energy_reconstructed_reconstruction_fraction")

    hist2d_energy_reconstructed_loglikelihood = ROOT.TH2D("hist2d_energy_reconstructed_loglikelihood", "hist2d_energy_reconstructed_loglikelihood;energy_reconstructed (keV);loglikelihood", 4096, 0, 4096 * 5, 2048, -100.0, 10.0)
    cetree_cutapplied.Draw("TMath::Log(likelihood):energy_reconstructed >> hist2d_energy_reconstructed_loglikelihood")

    hist2d_scattering_angle = ROOT.TH2D("hist2d_scattering_angle", "hist2d_scattering_angle;scattering_angle (deg.);scattering_direction_angle (deg.)", 512, 0, 180, 512, 0, 180)
    cetree_cutapplied.Draw("scattering_direction_angle * 180 / TMath::Pi():scattering_angle * 180 / TMath::Pi() >> hist2d_scattering_angle")

    Ndet = cetree_cutapplied.GetEntries()
    Aeff = Asim * Ndet / Nsim
    ARM_FWHM = calFWHM.getFWHMhist(hist_ARM)
    energy_FWHM = calFWHM.getFWHMhist(hist_energy)

    results = {}
    results["ini_energy"] = ini_energy
    results["Nsim"] = Nsim
    results["Ndet"] = Ndet
    results["Aeff"] = Aeff 
    results["ARM_FWHM"] = ARM_FWHM 
    results["energy_FWHM"] = energy_FWHM 

    print("Ndet : {}".format(Ndet))
    print("effective area (cm2) : {}".format(Aeff))
    print("ARM FWHM (deg.) : {}".format( ARM_FWHM ))
    print("energy resolution FWHM (keV) : {}".format( energy_FWHM ))

    with open(outfilename.replace(".root", ".json"), mode='wt', encoding='utf-8') as f:
        json.dump(dict(parfile, **results), f, ensure_ascii=False, indent=4)

    outfile.cd()

    hist_ARM.Write()
    hist_num_hits.Write()
    hist_energy.Write()
    hist_total_energy_deposit.Write()
    hist_scattering_angle.Write()
    hist_hit1_energy.Write()
    hist_hit2_energy.Write()
    hist_hit1_posx.Write()
    hist_hit1_posy.Write()
    hist_hit1_posz.Write()
    hist_hit2_posx.Write()
    hist_hit2_posy.Write()
    hist_hit2_posz.Write()
    hist_first_interaction_distance.Write()
    hist_reconstruction_fraction.Write()
    hist_loglikelihood.Write()
    hist_escape_flag.Write()
    hist_segment_flag.Write()
    hist2d_ARM_energy_reconstructed.Write()
    hist2d_ARM_total_energy_deposit.Write()
    hist2d_ARM_scattering_angle.Write()
    hist2d_ARM_hit1_energy.Write()
    hist2d_ARM_hit2_energy.Write()
    hist2d_ARM_first_interaction_distance.Write()
    hist2d_ARM_reconstruction_fraction.Write()
    hist2d_ARM_loglikelihood.Write()
    hist2d_energy_reconstructed_total_energy_deposit.Write()
    hist2d_energy_reconstructed_scattering_angle.Write()
    hist2d_energy_reconstructed_hit1_energy.Write()
    hist2d_energy_reconstructed_hit2_energy.Write()
    hist2d_energy_reconstructed_first_interaction_distance.Write()
    hist2d_energy_reconstructed_reconstruction_fraction.Write()
    hist2d_energy_reconstructed_loglikelihood.Write()
    hist2d_scattering_angle.Write()

    outfile.Close()

if __name__=="__main__":
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    parfilename = sys.argv[3]
    ini_energy = float(sys.argv[4])
    main(infilename, outfilename, parfilename, ini_energy)
