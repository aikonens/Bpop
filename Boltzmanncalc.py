import argparse
import pandas as pd
from math import e

### CONSTANTS
R_dict = {'kcal': 0.00198720, 'kJ': 0.00831446}
auconv_dict = {'kcal': 627.51, 'kJ': 2625.50} 
euler = e

class Bpop(object):

    def __init__(self, energies=[0.0], Tlist=[298.15], names=['com1'], R=0.00198720, units='kcal', etype='rel'):
        self.energies = energies
        self.Tlist = Tlist
        self.names = names
        self.units = units
        self.R = R_dict[self.units]
        self.conv = auconv_dict[self.units]
        self.etype = etype
        self.bdf = self.boltzmannDF()

    def boltzmannDF(self):
        Tlist = self.Tlist
        names = self.names
        R = self.R
        units = self.units
        origen = self.energies
        etype = self.etype
        Tlist = sorted(Tlist, key = lambda x:float(x))
        if etype == 'rel':
            Boltzdict = {"Name": names, f"∆G ({units}/mol)": origen}
            energies = origen
        elif etype == 'abs':
            energies = self.calcRel()
            Boltzdict = {"Name": names, 'G (a.u.)': origen, f"∆G ({units}/mol)": energies}
        rawcolumns = []
        for T, dG in [(T,dG) for T in Tlist for dG in energies]:
            Wraw = euler**(-dG / (R * T))
            rawname = f"Raw-{T}"
            boltzname = f"Boltzmann-{T}" 
            try:
                Boltzdict[rawname].append(round(Wraw, 4))
            except KeyError:
                Boltzdict[rawname] = [round(Wraw, 4)]
                Boltzdict[boltzname] = []
                rawcolumns.append(rawname)
        for rawcolumn in rawcolumns:
            bcolumn = rawcolumn.replace("Raw", "Boltzmann")
            for raw in Boltzdict[rawcolumn]:
                boltz = raw / sum(Boltzdict[rawcolumn])
                Boltzdict[bcolumn].append(round(boltz, 4))
            Boltzdict.pop(rawcolumn, None)
        return pd.DataFrame(Boltzdict)
    
    def calcRel(self):
        absoG = self.energies
        conv = self.conv
        minG = min(absoG)
        calcG = [round((ag - minG)*conv, 2) for ag in absoG]
        return calcG

    def Gconf(self):
        df = self.df
        Tlist = self.Tlist
        pass
        # return Gconf

CLI=argparse.ArgumentParser()
CLI.add_argument(
  "-dG","--relG",  # name on the CLI - drop the `--` for positional/required parameters
  nargs="*",  # 0 or more values expected => creates a list
  type=float,
  default=[],  # default if nothing is provided
  help="Give G values as space separated list",
)
CLI.add_argument(
  "-G","--absG",  # name on the CLI - drop the `--` for positional/required parameters
  nargs="*",  # 0 or more values expected => creates a list
  type=float,
  default=[],  # default if nothing is provided
  help="Give G values (a.u.) as space separated list",
)
CLI.add_argument(
  "-T","--temperature",  # name on the CLI - drop the `--` for positional/required parameters
  nargs="*",  # 0 or more values expected => creates a list
  type=float,
  default=[298.15],  # default if nothing is provided
  help="Give a list of temperatures in kelvins",
)
CLI.add_argument(
  "-N","--names",  # name on the CLI - drop the `--` for positional/required parameters
  nargs="*",  # 0 or more values expected => creates a list
  type=str,
  default=[],  # default if nothing is provided
  help="Give an identifier for the energies",
)
CLI.add_argument(
  "-u","--units",  # name on the CLI - drop the `--` for positional/required parameters
#   nargs=1,  # 0 or more values expected => creates a list
  type=str,
  default='kcal',  # default if nothing is provided
  help="Give unit system: [kcal]/kJ",
)

def main():
    args = CLI.parse_args()
    if args.relG:
        energies = args.relG
        etype = 'rel'
    elif args.absG:
        energies = args.absG 
        etype = 'abs'
        print(f"We use {etype} energies")
    else:
        raise ValueError('No energies provided, nothing to do.')
    if args.names and len(args.names) == len(energies):
        names = args.names
    else:
        names = energies
    # R = R_dict[args.units]
    # conv = auconv_dict[args.units]
    # access CLI options
    bpop = Bpop(energies=energies, Tlist=args.temperature, names=names, units=args.units, etype=etype)
    # Boltzdf = bpop.boltzmannDF(energies=energies, Tlist=args.temperature, names=names, R=R, units=args.units, etype=etype)
    Boltzdf = bpop.boltzmannDF()
    print(Boltzdf)

if __name__ == '__main__':
    main()