#/usr/bin/python3
from xmrpoolAPI import *
import sys, getopt

def printHelp():
    print("----------------------------",
          "  xmrpool.eu Stat Visualizer",
          "           by Exyss",
          "",
          "DESCRIPTION",
          "  Fast visualization of all the statistics linked to a wallet",
          "  that was at least once linked to a miner used on xmrpool.eu",
          "",
          "USAGE",
          "  xmrpool-check.py -h | --help",
          "     Display help prompt",
          "",
          "  xmrpool-check.py -a <wallet_address>",
          "     Display this wallet's worker stats",
          sep="\n")

if __name__ == "__main__":

    # get env variables
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "ha:", ["help"])
    except getopt.GetoptError:
        print("Incorrect usage, use 'xmrpool-check.py -h' to see correct usage")
        sys.exit(2)

    print(len(opts), opts)
    if('-h' in opts[1][0] or '-a' in opts[1][0]):
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                printHelp()
                sys.exit()

            elif opt == "-a":
                address = arg
                data = getWalletData(address)
                if 'error' in data:
                    print("[ERROR]", data['error'])
                    sys.exit(1)
                else:
                    payments = data['payments']
                    workers = getWorkers(data)

                    for worker in workers:
                        print(worker)
    else:
        print("Incorrect usage, use 'xmrpool-check.py -h' to see correct usage")