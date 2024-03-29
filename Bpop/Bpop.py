import argparse
import pandas as pd
from math import e, log

### CONSTANTS
R_dict = {'kcal': 0.00198720, 'kJ': 0.00831446}
auconv_dict = {'kcal': 627.51, 'kJ': 2625.50} 
euler = e

class Bpop(object):

    def __init__(self, 
                energies: list=[0.0], 
                Tlist: list=[298.15], 
                names: list=['com1'], 
                R: float=0.00198720, 
                units: str='kcal', 
                etype: str='rel'):
    
        '''
        Compute the Boltzmann weighs, Boltzmann weighed energies, and ensemble free energies
        Input energies are expected to be in hartrees (a.u.)
        return : dataframe, dG_Boltz, dG_conf, dG_Boltz_dGconf
        '''

        self.energies = energies
        self.Tlist = Tlist
        self.names = names
        self.units = units
        self.R = R_dict[self.units]
        self.conv = auconv_dict[self.units]
        self.etype = etype
        self.bdf = self.boltzmannDF()

    def boltzmannDF(self) -> pd.DataFrame:
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
                # Boltzdict[bcolumn].append(round(boltz, 4))
                Boltzdict[bcolumn].append(boltz)
            Boltzdict.pop(rawcolumn, None)
        return pd.DataFrame(Boltzdict)
    
    def calcRel(self) -> float:
        absoG = self.energies
        conv = self.conv
        minG = min(absoG)
        calcG = [round((ag - minG)*conv, 2) for ag in absoG]
        return calcG

    def Gmin(self) -> float:
        if self.etype == 'rel':
            raise ValueError('Only relative energies supplied, we need absolute energies') 
        return min(self.energies)

    def Gboltz(self) -> list:
        '''
        Return a list of Gboltz(T) values and list of Gfinal(T) values,
        where Gboltz is the Boltzmann weighed absolute Gibbs free energy at temperature T and
        Gfinal is Gboltz + Gconf.
        '''
        if self.etype == 'rel':
            raise ValueError('Only relative energies supplied, we need absolute energies') 
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
            bwgf = Gconfs[i] / conv
            bwgf = bwg + Gconfs[i] / conv 
            Gboltzs.append(round(bwg, 7))
            Gfinals.append(round(bwgf, 7))
        return Gboltzs, Gfinals

    def Gconf(self) -> list:
        '''
        Return a list of Gconf(T) values,
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
                try:
                    wsum += w*log(w)
                except ValueError:
                    print("Boltzmann weigh is <0.01%, skipping.")
            Sconf = -R * wsum
            Gconf = round(-T*Sconf, 4)
            Gconfs.append(Gconf)
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
CLI.add_argument(
  "-o","--out",  # name on the CLI - drop the `--` for positional/required parameters
  nargs="*",  # 0 or more values expected => creates a list
  type=str,
  default='bpop',  # default if nothing is provided
  help="Write output to a file, indicate name after keyword",
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
        raise AttributeError('No energies provided, nothing to do.')
    if args.names and len(args.names) == len(energies):
        names = args.names
    else:
        names = energies
    Tlist = args.temperature
    Tlist = sorted(Tlist, key = lambda x:float(x))
    bpop = Bpop(energies=energies, Tlist=Tlist, names=names, units=args.units, etype=etype)
    Boltzdf = bpop.boltzmannDF()
    Gconf = bpop.Gconf()
    print(Boltzdf)
    printlines = '-------------\nThermochemical data\n-------------\n' 
    for T, gc in zip(Tlist, Gconf):
        printlines += f'Gconf({T} K) = {gc} {args.units}/mol\n'
    if etype == 'abs':
        printlines += '-------------\nLowest energy conformer Gibbs free energies\n-------------\n'
        Gmin = bpop.Gmin()
        printlines += f'Gmin = {Gmin} a.u.\n'
        printlines += '-------------\nBoltzmann weighed Gibbs free energies\n-------------\n'
        Gboltz, Gfinals = bpop.Gboltz()
        for T, gb in zip(Tlist, Gboltz):
            printlines += f'Gboltz({T} K) = {gb} a.u.\n'
        printlines += '-------------\nFinal values with Gconf\n-------------\n'  
        for T, gf in zip(Tlist, Gfinals):
            printlines += f'Gboltz({T} K) = {gf} a.u.\n'
    print(printlines)
    if args.out:
        outname = args.out
        Boltzdf.to_csv(f'{outname}.csv')
        with open(f'{outname}.out', 'w') as f:
            f.write(printlines)

if __name__ == '__main__':
    main()