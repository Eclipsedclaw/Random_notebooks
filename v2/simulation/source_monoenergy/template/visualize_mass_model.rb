#! /usr/bin/env ruby

require 'comptonsoft'

def run_simulation(num, energy)
#  energy = 2000.0 # keV

  sim = ComptonSoft::Simulation.new
  sim.random_seed = 0
  sim.set_gdml "database/mass_model.gdml"
  sim.set_primary_generator :PlaneWavePrimaryGen, {
    particle: "gamma",
    photon_index: 2.0,
    energy_min: energy,
    energy_max: energy,
    position: vec(0.0, 0.0, 110.0),
    direction: vec(0.0, 0.0, -1.0),
    radius: 110.0
  }

  sim.visualize(mode: 'OGLSQt')
  sim.run(num)
end

### main ###
num = 25
energy = 2000.0 # keV
run_simulation(num, energy)
