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

  sim.set_primary_generator :PlaneWavePrimaryGen, {
    particle: "gamma",
    photon_index: 2.0,
    energy_min: 500.0,
    energy_max: 15000.0,
    position: vec(0.0, 0.0, 110.0),
    direction: vec(0.0, 0.0, -1.0),
    radius: 110.0
  }

  #sim.visualize(mode: 'OGLSQt')
  sim.run(num)
end

### main ###
num = 10000000
output = "source.root"
random = 0
run_simulation(num, random, output)
