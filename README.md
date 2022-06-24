# Bpop
A very simple Boltzmann population calculator for user supplied relative energies. Outputs a pandas dataframe.

usage: __main__.py [-h] [-dG [RELG [RELG ...]]] [-G [ABSG [ABSG ...]]] [-T [TEMPERATURE [TEMPERATURE ...]]] [-N [NAMES [NAMES ...]]] [-u UNITS]
                   [-o [OUT [OUT ...]]]

optional arguments:

  -h, --help            show this help message and exit
	
  -dG [RELG [RELG ...]], --relG [RELG [RELG ...]]
                        Give G values as space separated list
												
  -G [ABSG [ABSG ...]], --absG [ABSG [ABSG ...]]
                        Give G values (a.u.) as space separated list
												
  -T [TEMPERATURE [TEMPERATURE ...]], --temperature [TEMPERATURE [TEMPERATURE ...]]
                        Give a list of temperatures in kelvins
												
  -N [NAMES [NAMES ...]], --names [NAMES [NAMES ...]]
                        Give an identifier for the energies
												
  -u UNITS, --units UNITS
                        Give unit system: [kcal]/kJ
												
  -o [OUT [OUT ...]], --out [OUT [OUT ...]]
                        Write output to a file, indicate name after keyword
