#! /usr/bin/env ruby
require 'comptonsoft'

def run_simulation(num, random, output)

  sim = ComptonSoft::Simulation.new
  sim.output = output
  sim.random_seed = random
  sim.verbose = 0
  sim.print_detector_info
  sim.set_database(detector_configuration: "database/detector_configuration_2mm.xml",
                   detector_parameters: "database/detector_parameters_esol_aramaki.xml")
  sim.set_gdml "database/mass_model.gdml"
  sim.set_physics(hadron_hp: false, cut_value: 0.001)

  # --- HealPix
  ra_deg  = 0.0 # or l (deg)
  dec_deg = 90.0 # or b (deg)
  # --- atmosphere bkg
  fits_filename_source = "../../expacs/fitsfile/AliceSprings_Australia_2021_3_21_alt30000m_map_photon.fits"

  ra  = ra_deg*Math::PI/180.0
  dec = dec_deg*Math::PI/180.0
  sim.set_primary_generator :AllSkyPrimaryGen, {
    particle: "gamma",
    # --- spectrum
    energy_min: 500.0, # keV
    energy_max: 15000.0, # keV
    # --- image
    center_position: vec(0.0, 0.0, 0.0),
    distance: 110.0, #cm
    center_direction: vec(-Math::sin(0.5*Math::PI-dec)*Math::cos(ra), -Math::sin(0.5*Math::PI-dec)*Math::sin(ra), -Math::cos(0.5*Math::PI-dec)), # <- crab coordinate
    radius: 110.0 , # cm
    fits_filename: fits_filename_source,
    hdunum: 2,
    detector_roll_angle: 0.0,
    set_polarization: false,
  }

  #sim.visualize(mode: 'OGLSQt')
  sim.run(num)
end

### main ###
num = 50000000
output = "bkg.root"
random = 0
run_simulation(num, random, output)
