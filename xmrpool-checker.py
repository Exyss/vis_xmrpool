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

def formatTotalStatsTable(totalStats):
    table =  "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("PENDING BALANCE", totalStats['balance']+" XMR", "TOTAL PAID", totalStats['paid']+" XMR")
    table += "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("LAST REWARD", totalStats['lastReward']+" XMR", "TOTAL HASHES", totalStats['hashes'])
    table += "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("LAST SHARE", totalStats['lastShare'], "TOTAL HASHRATE", totalStats['hashrate'])
    return table

def formatWorkersTable(workers):
    table = " {:^21}   {:^14}   {:^16}   {:^16}   {:^16}   {:^19}\n".format("WORKER ID", "HASHRATE", "HASHES", "EXPIRED", "INVALID", "LAST SHARE")
    table += " {:^21}   {:^14}   {:^16}   {:^16}   {:^16}   {:^19}\n".format("-"*21, "-"*14, "-"*16, "-"*16, "-"*16, "-"*19)
    for worker in workers:
        table += " {:<21}   {:^14}   {:>16}   {:>16}   {:>16}   {:^19}\n".format(" "+worker['workerId'], worker['hashrate'], worker['hashes']+" ", worker['expired']+" ", worker['invalid']+" ", worker['lastShare'])
    return table

def formatPaymentsTable(payments):
    table = " {:^49}   {:^21}   {:^19}   {:^19}\n".format("TRANSACTION HASH", "AMOUNT", "DATE", "MIXIN")
    table += " {:^49}   {:^21}   {:^19}   {:^19}\n".format("-"*49, "-"*21, "-"*19, "-"*19)
    for payment in payments:
        table += " {:^49}   {:^21}   {:^19}   {:^19}\n".format(payment['hash'], payment['amount']+"€", payment['date'], payment['mixin'])
    return table

if __name__ == "__main__":

    if(len(sys.argv[1:]) > 0):  #if no argument was passed
        # get env variables
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "ha:swp", ["help", "address", "stats", "workers", "payments"])
        except getopt.GetoptError:
            print("Incorrect usage, use 'xmrpool-check.py -h' to see correct usage")
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                printHelp()
                break
            elif opt in ("-a", "--address="):
                address = arg
                data = getWalletData(address)
                print("\n")

                if 'error' in data:
                    print("[ERROR]", data['error'])
                    sys.exit(1)
                else:
                    if len(opts) == 1:
                        print(formatTotalStatsTable(getTotalStats(data)))
                        print(formatWorkersTable(getWorkers(data)))
                        print(formatPaymentsTable(getPayments(data)))
                    else:
                        options = {"s": False, "w": False, "p": False}
                        for opt, _ in opts:
                            if opt in ("-s", "--stats"): options['s'] = True
                            if opt in ("-w", "--workers"): options['w'] = True
                            if opt in ("-p", "--payments"): options['p'] = True
                        if(options['s'] == True): print(formatTotalStatsTable(getTotalStats(data)))
                        if(options['w'] == True): print(formatWorkersTable(getWorkers(data)))
                        if(options['p'] == True): print(formatPaymentsTable(getPayments(data)))
                break
    else:
        print("Incorrect usage, use 'xmrpool-check.py -h' to see correct usage")
        sys.exit(2)