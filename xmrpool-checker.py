# Get the latest version here: https://github.com/Exyss/xmrpool-check.git
#/usr/bin/python3
from xmrpoolAPI import *
from time import sleep
from sys import exit
import getopt 

def printHelp():
    print("---------------------------------",
          "    xmrpool.eu Stat Checker",
          "               by Exyss",
          "",
          "DESCRIPTION",
          "\tFast visualization of all the statistics linked to a wallet",
          "\tthat was at least once linked to a miner used on xmrpool.eu",
          "",
          "USAGE",
          "\t-h, --help",
          "\t\tDisplay help prompt.",
          "",
          "\t-a <wallet_address>",
          "\t\tSame all info linked to this wallet.",
          "",
          "\t-a <wallet_address> [-s, --stats][-w, --workers][-p, --payments][-t, --time <seconds>]",
          "\t\tDisplay only the defined set of info. If a time interval was set, the program",
          "\t\twill repeat after the defined interval has passed. To stop it, use Ctrl+C.",
          sep="\n")

def formatTotalStatsTable(totalStats):
    table =  "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("PENDING BALANCE", totalStats['balance']+" XMR", "TOTAL HASHRATE", totalStats['hashrate'])
    table += "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("TOTAL PAID", totalStats['paid']+" XMR", "TOTAL HASHES", totalStats['hashes'])
    table += "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("LAST REWARD", totalStats['lastReward']+" XMR", "TOTAL EXPIRED", totalStats['expired'])
    table += "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("LAST SHARE", totalStats['lastShare'], "TOTAL INNVALID", totalStats['invalid'])
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
            opts, _ = getopt.getopt(sys.argv[1:], "ha:swpt:", ["help", "address=", "stats", "workers", "payments", "time="])
        except getopt.GetoptError:
            print("Incorrect usage, use 'xmrpool-check.py -h' to see correct usage")
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                printHelp()
                break
            elif opt in ("-a", "--address"):
                address = arg
                data = getWalletData(address)
                print() #newline

                if 'error' in data:
                    print("[ERROR]", data['error'])
                    sys.exit(1)
                else:
                    options = {}
                    for opt, arg in opts:   # get bonus options
                        if opt in ("-s", "--stats"): options['s'] = True
                        if opt in ("-w", "--workers"): options['w'] = True
                        if opt in ("-p", "--payments"): options['p'] = True
                        if opt in ("-t", "--time"): options['t'] = int(arg)

                    while True:
                        if('s' not in options and 'w' not in options and 'p' not in options):   # if no flag is set, print all of them
                            print(formatTotalStatsTable(getTotalStats(data)))
                            print(formatWorkersTable(getWorkers(data)))
                            print(formatPaymentsTable(getPayments(data)))
                        else:
                            if('s' in options): print(formatTotalStatsTable(getTotalStats(data)))
                            if('w' in options): print(formatWorkersTable(getWorkers(data)))
                            if('p' in options): print(formatPaymentsTable(getPayments(data)))

                        if('t' in options): # repeat if time interval was set
                            sleep(options['t'])
                            print("\n\n")
                        else: break
                break
    else:
        print("Incorrect usage, use 'xmrpool-check.py -h' to see correct usage")
        sys.exit(2)