#!/usr/bin/env python
# coding: UTF-8

import sys
import healpy as hp
import pandas as pd
import numpy as np

nside = 32
min_energy = 0.2
max_energy = 50.0

do_multi_solid_angle = True

def make_flux_map(nside, df, particle, energy):
    _df = df.query('particle == "{}" & energy == {}'.format(particle, energy))
    costhetas = _df['costheta'].values
    delta_costheta = 2.0/(len(costhetas) - 1)
    fluxes = _df['flux'].values

    npix = hp.nside2npix(nside)
    flux_map = np.zeros(npix)

    for ipix in range(npix):
        ang = hp.pix2ang(nside, ipix, nest=False)
        costheta = np.cos(ang[0])

        flux = 0
        if costheta >= 1.0 - delta_costheta:
            flux = fluxes[-2]
        else:
            index_costheta = int((costheta + 1)/delta_costheta)
            fraction = (costheta + 1)/delta_costheta - index_costheta
            flux = (1.0 - fraction) * fluxes[index_costheta] + fraction * fluxes[index_costheta + 1] 
        
        flux_map[ipix] = flux

    if do_multi_solid_angle:
        flux_map *= hp.nside2pixarea(nside)

    return flux_map

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
    _df = df.query('particle == "{}"'.format(particle))
    energies = np.sort(np.unique(_df['energy']))

    flux_maps = []
    column_names = []
    column_units = []
    extra_header = []
    index = 1
    for energy in energies:
        if min_energy < energy < max_energy:
            flux_map = make_flux_map(nside, df, "photon", energy)
            flux_maps.append(flux_map)
            column_names.append("map_E_{}_MeV".format(energy))
            if do_multi_solid_angle:
                column_units.append('ph/cm2/MeV/s')
            else:
                column_units.append('ph/cm2/MeV/sr/s')
            extra_header += [('ENE{}'.format(index), energy, "MeV")]
            index += 1
    extra_header += [('NMAP', index-1)]

    inputparam = get_inputparaminfo(infilename, df)
    place = inputparam["place"]
    date = inputparam["date"]
    lat = inputparam["lat"]
    lon = inputparam["lon"]
    alti = inputparam["alti"]
    extra_header += [ \
                    ('MINENE', min_energy, 'MeV'), \
                    ('MAXENE', max_energy, 'MeV'), \
                    ('particle', particle), \
                    ('place', place), \
                    ('date', date), \
                    ('lati', lat, 'deg'), \
                    ('long', lon, 'deg'), \
                    ('alti', alti, 'km'), \
                    ('CALSANG', do_multi_solid_angle , 'The solid angle of a pixel is considered or not')
                   ]

    hp.fitsfunc.write_map(outfilename, flux_maps, \
                          nest=False, column_names=column_names, column_units=column_units, \
                          extra_header = extra_header)

if __name__=="__main__":
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    particle = sys.argv[3]
    main(infilename, outfilename, particle)
