import argparse
import pandas as pd
from math import e, log

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
        # Tlist = sorted(Tlist, key = lambda x:float(x))
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

    def Gboltz(self):
        '''
        Return a list of lists consisting of [T, Gboltz(T)] pairs, and [T, Gfinal(T)] pairs,
        where Gboltz is the Boltzmann weighed absolute Gibbs free energy at temperature T and
        Gfinal is Gboltz + Gconf.
        '''
        df = self.bdf
        R = self.R
        Tlist = self.Tlist
        Gconfs = self.Gconf()
        conv = self.conv
        Gboltzs = []
        Gfinals = []
        for i, T in enumerate(Tlist):
            bwg = 0
            for ag, bw in zip(df['G (a.u.)'], df[f"Boltzmann-{T}"]):
                bwg += ag * bw
            bwgf = Gconfs[i][1] / conv
            bwgf = bwg + Gconfs[i][1] / conv 
            Gboltzs.append([T, round(bwg, 7)])
            Gfinals.append([T, round(bwgf, 7)])
        return Gboltzs, Gfinals

    def Gconf(self):
        '''
        Return a list of lists consisting of [T, Gconf(T)] pairs,
        where Gconf is the Gibbs-Shannon entropy, Sconf, contribution in specific temperature T. 
        '''
        df = self.bdf
        R = self.R
        Tlist = self.Tlist
        Gconfs = []
        for T in Tlist:
            wsum = 0
            colname = f"Boltzmann-{T}"
            for w in df[colname]:
                wsum += w*log(w)
            Sconf = -R * wsum
            Gconf = round(-T*Sconf, 4)
            Gconfs.append([T, Gconf])
        return Gconfs

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
    Tlist = args.temperature
    Tlist = sorted(Tlist, key = lambda x:float(x))
    bpop = Bpop(energies=energies, Tlist=Tlist, names=names, units=args.units, etype=etype)
    # Boltzdf = bpop.boltzmannDF(energies=energies, Tlist=args.temperature, names=names, R=R, units=args.units, etype=etype)
    Boltzdf = bpop.boltzmannDF()
    Gconf = bpop.Gconf()
    print(Boltzdf)
    print('-------------')
    print('Thermochemical data')
    print('-------------')
    for gc in Gconf:
        print(f'Gconf({gc[0]} K) = {gc[1]} {args.units}/mol')
    if etype == 'abs':
        print('-------------')
        print('Boltzmann weighed Gibbs free energies')
        print('-------------')
        Gboltz, Gfinals = bpop.Gboltz()
        for gb in Gboltz:
            print(f'Gboltz({gb[0]} K) = {gb[1]} a.u.')
        print('-------------')
        print('Final values with Gconf')
        print('-------------')   
        for gf in Gfinals:
            print(f'Gboltz({gf[0]} K) = {gf[1]} a.u.') 

if __name__ == '__main__':
    main()