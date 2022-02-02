import argparse
import pandas as pd

### CONSTANTS
Rgas = 0.00198720 # kcal/mol
euler = 2.718281828459045

def boltzmann(dGlist, Tlist, names):
    Tlist = sorted(Tlist, key = lambda x:float(x))
    Boltzdict = {"Name": names, "∆G (kcal/mol)": dGlist}
    rawcolumns = []
    for T, dG in [(T,dG) for T in Tlist for dG in dGlist]:
        Wraw = euler**(-dG / (Rgas * T))
        rawname = "Raw-" + str(T)
        boltzname = "Boltzmann-" + str(T) 
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

CLI=argparse.ArgumentParser()
CLI.add_argument(
  "-g","--relg",  # name on the CLI - drop the `--` for positional/required parameters
  nargs="*",  # 0 or more values expected => creates a list
  type=float,
  default=[0.0],  # default if nothing is provided
  help="Give ∆G [kcal/mol] values as space separated list",
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

def main():
    args = CLI.parse_args()
    if args.names and len(args.names) == len(args.relg):
        names = args.names
    else:
        names = args.relg
    # access CLI options
    Boltzdf = boltzmann(args.relg, args.temperature, names)
    print(Boltzdf)

if __name__ == '__main__':
    main()