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
                        
Example usage and output.

$ python Boltzmanncalc.py --relg 0.0 0.44 1.71 -T 273.15 298.15 373.15 -N c1 c2 c3

  Name  ∆G (kcal/mol)  Boltzmann-273.15  Boltzmann-298.15  Boltzmann-373.15
0   c1           0.00            0.6723            0.6529            0.6053
1   c2           0.44            0.2989            0.3107            0.3344
2   c3           1.71            0.0288            0.0364            0.0603
