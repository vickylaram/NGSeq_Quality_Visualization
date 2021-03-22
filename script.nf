process setUpCondaEnv {
  conda './ngs_seq_visualisation.yaml'

  '''
  your_command --here
  '''
}

process runFastQC {
  conda '/some/path/my-env.yaml'

  '''
  your_command --here
  '''
}

process visualize {

'''
run dash script
'''

}
