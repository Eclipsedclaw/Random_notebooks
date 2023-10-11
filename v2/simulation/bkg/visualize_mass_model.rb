#! /usr/bin/env ruby

require 'comptonsoft'

def run_simulation(num)
  energy = 2000.0 # keV

  sim = ComptonSoft::Simulation.new
  sim.random_seed = 0
  sim.set_gdml "database/mass_model.gdml"
  sim.set_primary_generator :IsotropicPrimaryGen, {
    particle: "gamma",
    photon_index: 2.0,
    energy_min: energy,
    energy_max: energy,
    center_position: vec(0.0, 0.0, 0.0),
    center_direction: vec(0.0, 0.0, 1.0),
    radius: 110.0,
    distance: 110.0
  }

  sim.visualize(mode: 'OGLSQt')
  sim.run(num)
end

### main ###
num = 25
run_simulation(num)
