#!/usr/bin/env ruby

require 'comptonsoft'

class MyApp < ANL::ANLApp
  attr_accessor :inputs, :output

  def setup()
    add_namespace ComptonSoft

    chain :CSHitCollection
    chain :ConstructDetector
    with_parameters(detector_configuration: "database/detector_configuration_2mm.xml", verbose_level: 1)
    chain :ReadHitTree
    with_parameters(file_list: @inputs)
    chain :EventReconstruction
    with_parameters(max_hits: 8,
                    reconstruction_method: "HY2020",
                    source_distant: true,
                    source_direction: vec(0.0, 0.0, 1.0),
                    parameter_file: "parfile_HY2020.json")
    chain :HistogramEnergy2D
    with_parameters(number_of_bins: 512,
                    energy_min: 0.0,
                    energy_max: 2500.0)
    chain :HistogramARM
    with_parameters(number_of_bins: 500,
                    range_min: -25.0,
                    range_max: 25.0)
    chain :WriteComptonEventTree
    chain :SaveData
    with_parameters(output: @output)
  end
end

### main ###
app = MyApp.new
app.inputs = [ "bkg.root" ]
app.output = "cetree_bkg.root"
app.run(:all, 10000)
