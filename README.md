# Bpop
A very simple Boltzmann population calculator for user supplied relative energies. Outputs a pandas dataframe.

usage: Boltzmanncalc.py [-h] [-g [RELG ...]] [-T [TEMPERATURE ...]] [-N [NAMES ...]]

optional arguments:
  -h, --help            show this help message and exit
  -g [RELG ...], --relg [RELG ...]
                        Give ∆G [kcal/mol] values as space separated list
  -T [TEMPERATURE ...], --temperature [TEMPERATURE ...]
                        Give a list of temperatures in kelvins
  -N [NAMES ...], --names [NAMES ...]
                        Give an identifier for the energies
                        
Example:

$ python Boltzmanncalc.py --relg 0.0 0.44 1.71 -T 273.15 298.15 373.15 -N c1 c2 c3
