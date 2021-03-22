#!/usr/bin/env nextflow

process setUpCondaEnv {
  conda './ngs_seq_visualisation.yaml'

  println('conda env')

  '''
  your_command --here
  '''
}

process runFastQC {
  conda '/some/path/my-env.yaml'

  println('run fasted')

  '''
  your_command --here
  '''
}

process visualize {

println('visualize')

'''
run dash script
'''

}
