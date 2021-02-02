# Get the latest version here: https://github.com/Exyss/xmrpool-check.git
#/usr/bin/python3
from xmrpoolAPI import *
import sys, getopt

def printHelp():
    print("----------------------------",
          "  xmrpool.eu Stat Visualizer",
          "           by Exyss",
          "",
          "DESCRIPTION",
          "\tFast visualization of all the statistics linked to a wallet",
          "\tthat was at least once linked to a miner used on xmrpool.eu",
          "",
          "USAGE",
          "\t-h, --help",
          "\t\tDisplay help prompt",
          "",
          "\t-a <wallet_address>",
          "\t\tDisplay this wallet's worker stats",
          sep="\n")

def formatWorkersTable(workers):
    table = "{:^20}      {:^15}      {:^15}      {:^15}      {:^15}      {:^20}\n".format("WORKER ID", "HASHRATE", "HASHES", "EXPIRED", "INVALID", "LAST SHARE")
    table += "{:<20}      {:^15}      {:>15}      {:>15}      {:>15}      {:>20}\n".format("-"*20, "-"*15, "-"*15, "-"*15, "-"*15, "-"*20)
    for worker in workers:
        table += "{:<20}      {:^15}      {:>15}      {:>15}      {:>15}      {:^20}\n".format(worker['workerId'], worker['hashrate'], worker['hashes'], worker['expired'], worker['invalid'], worker['lastShare'])
    return table

if __name__ == "__main__":

    if(len(sys.argv[1:]) > 0):  #if no argument was passed
        # get env variables
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "ha:", ["help"])
        except getopt.GetoptError:
            print("Incorrect usage, use 'xmrpool-check.py -h' to see correct usage")
            sys.exit(2)

        opt, arg = opts[0]    # get first parameter

        if opt in ("-h", "--help"):
            printHelp()

        elif opt == "-a":
            address = arg
            data = getWalletData(address)
            if 'error' in data:
                print("[ERROR]", data['error'])
                sys.exit(1)
            else:
                payments = data['payments']
                print(formatWorkersTable(getWorkers(data)))
        else:
            print("Incorrect usage, use 'xmrpool-check.py -h' to see correct usage")
    else:
        print("Incorrect usage, use 'xmrpool-check.py -h' to see correct usage")