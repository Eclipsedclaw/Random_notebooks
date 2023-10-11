#!/usr/bin/env python
# coding: UTF-8

import sys
import ROOT
import json 

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(53)

def main(infilename, _ini_energy = -1):
#    infilename = "E_1000.root"
    parfilename = infilename.replace(".root", ".json")
    infile = ROOT.TFile(infilename, "r")
    
    ini_energy = _ini_energy
    if ini_energy == -1:
        with open(parfilename, "r") as f:
            parfile = json.load(f)
            ini_energy = parfile["ini_energy"]

    canvas = ROOT.TCanvas("c", "c", 900, 800)
    canvas.Divide(3, 4)
    canvas_index = 0

    canvas_index += 1
    canvas.cd(canvas_index)
    infile.Get("hist_ARM").Draw()

    canvas_index += 1
    canvas.cd(canvas_index)
    _ = infile.Get("hist_energy")
    _.GetXaxis().SetRangeUser(0, ini_energy * 1.5)
    _.Draw()

    canvas_index += 1
    canvas.cd(canvas_index)
    infile.Get("hist2d_scattering_angle").Draw("colz")

    canvas_index += 1
    canvas.cd(canvas_index)
    _ = infile.Get("hist_total_energy_deposit")
    _.GetXaxis().SetRangeUser(0, ini_energy * 1.5)
    _.Draw()

    canvas_index += 1
    canvas.cd(canvas_index)
    infile.Get("hist_scattering_angle").Draw()

    canvas_index += 1
    canvas.cd(canvas_index)
    _ = infile.Get("hist_hit1_energy")
    _.GetXaxis().SetRangeUser(0, ini_energy * 1.5)
    _.Draw()

    canvas_index += 1
    canvas.cd(canvas_index)
    _ = infile.Get("hist_hit2_energy")
    _.GetXaxis().SetRangeUser(0, ini_energy * 1.5)
    _.Draw()

    canvas_index += 1
    canvas.cd(canvas_index)
    _ = infile.Get("hist_first_interaction_distance")
    _.GetXaxis().SetRangeUser(0, 50.0)
    _.Draw()

    canvas_index += 1
    canvas.cd(canvas_index)
    _ = infile.Get("hist2d_ARM_energy_reconstructed")
    _.GetYaxis().SetRangeUser(0, ini_energy * 1.5)
    _.Draw("colz")

    canvas_index += 1
    canvas.cd(canvas_index)
    infile.Get("hist2d_ARM_scattering_angle").Draw("colz")

    canvas_index += 1
    canvas.cd(canvas_index)
    _ = infile.Get("hist2d_ARM_hit1_energy")
    _.GetYaxis().SetRangeUser(0, ini_energy)
    _.Draw("colz")

    canvas_index += 1
    canvas.cd(canvas_index)
    _ = infile.Get("hist2d_ARM_hit2_energy")
    _.GetYaxis().SetRangeUser(0, ini_energy)
    _.Draw("colz")

    canvas_index += 1
    canvas.cd(canvas_index)
    _ = infile.Get("hist2d_ARM_first_interaction_distance")
    _.GetYaxis().SetRangeUser(0, 50.0)
    _.Draw("colz")

    canvas.SaveAs(infilename.replace(".root", ".pdf"))
    canvas.SaveAs(infilename.replace(".root", ".png"))

if __name__=="__main__":
    infilename = sys.argv[1]
    if len(sys.argv) == 3:
        ini_energy = float(sys.argv[2])
        main(infilename, ini_energy)
    else:
        main(infilename)
