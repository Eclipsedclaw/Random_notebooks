#!/usr/bin/env python
# coding: UTF-8

import sys
import ROOT
import healpy as hp
import pandas as pd
import numpy as np

nside = 32
ref_energy = 1.0 #MeV
fit_range = [0.8, 15.0] #MeV

do_multi_solid_angle = True

do_draw_fit_result = False
dir_fit_result = "fit_result"
use_photonflux = True 

def make_spectrum_at_skyposition(nside, df, particle, theta, phi):
    _df = df.query('particle == "{}"'.format(particle))
    energies = np.sort(np.unique(_df['energy']))
    flux_spectrum = []

    costheta = np.cos(theta)
    delta_costheta = 2.0/(len(_df)/len(energies) - 1)
    for energy in energies:
        _df_tmp = _df.query('energy == {}'.format(energy)).sort_values('costheta')
        fluxes = _df_tmp['flux'].values
        if costheta >= 1.0 - delta_costheta:
            flux = fluxes[-2]
            flux_spectrum.append(flux)
        else:
            index_costheta = int((costheta + 1)/delta_costheta)
            fraction = (costheta + 1)/delta_costheta - index_costheta
            flux = (1.0 - fraction) * fluxes[index_costheta] + fraction * fluxes[index_costheta + 1] 
            flux_spectrum.append(flux)
    
    flux_spectrum = np.array(flux_spectrum)

    return energies, flux_spectrum

def fit_spectrum(energies, flux_spectrum, ref_energy, fit_range = [0.8, 15.0], sys_error_rate = 1e-2, nfit = 2, fitfigname = "test.png"): 
    tg_spectrum = ROOT.TGraphErrors(len(energies), energies, flux_spectrum, \
                                    np.zeros(len(energies)), flux_spectrum * sys_error_rate) 
    fit_func = ROOT.TF1("fit_func", "[0] * (x / {}) ** (-1 *[1])".format(ref_energy), fit_range[0], fit_range[1]) 
    fit_func.SetParameters(tg_spectrum.Eval(ref_energy), 1.5)
    for i in range(nfit):
        tg_spectrum.Fit(fit_func, "", "", fit_range[0], fit_range[1]) 

    norm = fit_func.GetParameter(0)
    index = fit_func.GetParameter(1)

    if do_draw_fit_result:
        c = ROOT.TCanvas("c", "c", 640, 480)
        c.SetLogx()
        c.SetLogy()
        tg_spectrum.Draw("A * L")
        fit_func.Draw("same")
        c.Draw()
        c.SaveAs(dir_fit_result + "/" + fitfigname)

    return norm, index

def calc_integrated_photonflux(norm, index, ref_energy, energy_range):
    intg1 = norm * ref_energy / (1 - index) * (energy_range[0] / ref_energy)**(1-index)
    intg2 = norm * ref_energy / (1 - index) * (energy_range[1] / ref_energy)**(1-index)
    return intg2 - intg1

def calc_integrated_energyflux(norm, index, ref_energy, energy_range):
    MeVtoErg = 1.602176565e-06
    intg1 = norm * ref_energy**2 / (2 - index) * (energy_range[0] / ref_energy)**(2-index)
    intg2 = norm * ref_energy**2 / (2 - index) * (energy_range[1] / ref_energy)**(2-index)
    return (intg2 - intg1) * MeVtoErg

def make_flux_pl_map(nside, df, particle, **kwargs):
    _df = df.query('particle == "{}"'.format(particle))
    npix = hp.nside2npix(nside)

    index_map = np.zeros(npix)
    norm_map = np.zeros(npix)
    ref_energy_map = np.zeros(npix)
    integrated_flux_map = np.zeros(npix)
    
    theta_before = -1
    norm, index = 1e-10, 0
    for ipix in range(npix):
        theta, phi = hp.pix2ang(nside, ipix, nest=False)
        if theta_before != theta:
            print(ipix,"/",npix)
            energies, flux_spectrum = make_spectrum_at_skyposition(nside, df, particle, theta, phi)
            if do_draw_fit_result:
                fitfigname = "fit_{}_theta{}deg".format(particle, theta * 180 / np.pi)
                for pg_key, pg_val in kwargs.items():
                    fitfigname += "_{}{}".format(pg_key, pg_val)
                fitfigname += ".png"
                norm, index = fit_spectrum(energies, flux_spectrum, ref_energy, fit_range, fitfigname = fitfigname)
            else:
                norm, index = fit_spectrum(energies, flux_spectrum, ref_energy, fit_range)
        index_map[ipix] = index
        norm_map[ipix] = norm
        ref_energy_map[ipix] = ref_energy
        if use_photonflux:
            integrated_flux_map[ipix] = calc_integrated_photonflux(norm, index, ref_energy, fit_range)
        else:
            integrated_flux_map[ipix] = calc_integrated_energyflux(norm, index, ref_energy, fit_range)
        theta_before = theta

    if do_multi_solid_angle:
        norm_map *= hp.nside2pixarea(nside)
        integrated_flux_map *= hp.nside2pixarea(nside)

    return norm_map, index_map, ref_energy_map, integrated_flux_map

def get_inputparaminfo(infilename, df):
    tmp = infilename.split("/")[-1].split("_")
    place = "{}-{}".format(tmp[0], tmp[1])

    years = np.sort(np.unique(df['year']))
    months = np.sort(np.unique(df['month']))
    days = np.sort(np.unique(df['day']))
    lats = np.sort(np.unique(df['lat(deg)']))
    lons = np.sort(np.unique(df['lon(deg)']))
    altis = np.sort(np.unique(df['alti(m)'])) / 1e3 # m => km
    gs = np.sort(np.unique(df['g']))
    
    for _ in [ years, months, days, lats, lons, altis, gs]:
        if len(_) > 1:
            print("WARNING: several input parameters are mixed. please check the background csv file.")

    return {"date": "{}-{}-{}".format(years[0], months[0], days[0]), "place": place, "lat": lats[0], "lon": lons[0], "alti": altis[0]}

def main(infilename, outfilename, particle):
    df = pd.read_csv(infilename)
    
    inputparam = get_inputparaminfo(infilename, df)
    place = inputparam["place"]
    date = inputparam["date"]
    lat = inputparam["lat"]
    lon = inputparam["lon"]
    alti = inputparam["alti"]
    extra_header = [ \
                    ('REFENE', ref_energy, 'MeV'), \
                    ('MINENE', fit_range[0] , 'MeV'), \
                    ('MAXENE', fit_range[1] , 'MeV'), \
                    ('particle', particle), \
                    ('place', place), \
                    ('date', date), \
                    ('lati', lat, 'deg'), \
                    ('long', lon, 'deg'), \
                    ('alti', alti, 'km'), \
                    ('CALSANG', do_multi_solid_angle , 'The solid angle of a pixel is considered or not')
                   ]

    norm_map, index_map, ref_energy_map, integrated_flux_map = make_flux_pl_map(nside, df, particle, place = place, date = date, alti = alti)
    column_names = ['Normalization', 'PhotonIndex', 'ReferenceEnergy', 'IntegratedFlux']
    if do_multi_solid_angle:
        if use_photonflux:
            column_units = ['ph/cm2/MeV/s', '', 'MeV', 'ph/cm2/s']
        else:
            column_units = ['ph/cm2/MeV/s', '', 'MeV', 'erg/cm2/s']
    else:
        if use_photonflux:
            column_units = ['ph/cm2/MeV/sr/s', '', 'MeV', 'ph/cm2/sr/s']
        else:
            column_units = ['ph/cm2/MeV/sr/s', '', 'MeV', 'erg/cm2/sr/s']

    hp.fitsfunc.write_map(outfilename, [norm_map, index_map, ref_energy_map, integrated_flux_map], \
                          nest=False, column_names=column_names, column_units=column_units, \
                          extra_header = extra_header)

if __name__=="__main__":
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    particle = sys.argv[3]
    if len(sys.argv) == 5:
        do_draw_fit_result = int(sys.argv[4])
    main(infilename, outfilename, particle)
