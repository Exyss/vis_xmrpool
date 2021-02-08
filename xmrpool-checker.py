#/usr/bin/python3
#Get the latest version here: https://github.com/Exyss/xmrpool-checker.git

from xmrpoolAPI import *
from time import sleep
import sys, getopt 

def printHelp():
    print("---------------------------------",
          "    xmrpool.eu Stat Checker",
          "               by Exyss",
          "",
          "DESCRIPTION",
          "\tTool for faster and more complete visualization of all the statistics linked",
          "\tto a wallet that was at least once linked to a miner used on xmrpool.eu.",
          "",
          "OPTIONS",
          "\t-h, --help",
          "\t\tDisplay help prompt.",
          "",
          "\t-a <wallet_address> [options]",
          "\t\tThis is a must use. Display info about the given wallet.",
          "\t\tWithout other options given, this command will print every",
          "\t\tinfo linked to the given wallet only once, without logging it",
          "",
          "\t-s, --stats",
          "\t\tDisplay only total statistics.",
          "",
          "\t-w, --workers",
          "\t\tDisplay only informations about workers.",
          "",
          "\t-p, --payments",
          "\t\tDisplay only informations about payments.",
          "",
          "\t-t, --time <seconds>",
          "\t\tRepeat the displaying every t seconds.",
          "",
          "\t-c, --counter <times>",
          "\t\tRepeat the displaying for c times. Must be used with -t.",
          "",
          "\t-l, --log",
          "\t\tLog the displayed data into a log file.",
          "\t\tLog files can be found in logs/",
          "",
          "\t-f, --full",
          "\t\tDisplay more informations.",
          sep="\n")

def getExtraOptions(opts):
    options = {'l': False, 'f': False}
    for opt, arg in opts:   # get bonus options
        if opt in ("-s", "--stats"): options['s'] = True
        if opt in ("-w", "--workers"): options['w'] = True
        if opt in ("-p", "--payments"): options['p'] = True
        if opt in ("-l", "--log"): options['l'] = True      # default is false
        if opt in ("-f", "--full"): options['f'] = True     # default is false
        if opt in ("-t", "--time"): options['t'] = int(arg)
        if opt in ("-c", "--counter"):
            if('t' in options):     # -t must be set if -c is used
                options['c'] = int(arg)
            else: raise Exception("-t must also be set in order to use -c")
    return options

def plotData(options):
    data = getWalletData(address)
    print() #newline

    if 'error' in data:
        print("[ERROR]", data['error'])
        sys.exit(1)
    else:

        if('s' not in options and 'w' not in options and 'p' not in options):   # if no flag is set, print all of them
            print(formatTotalStatsTable(getTotalStats(data), options['f']))
            print(formatWorkersTable(getWorkers(data), options['f']))
            print(formatPaymentsTable(getPayments(data), options['f']))
        else:
            if('s' in options): print(formatTotalStatsTable(getTotalStats(data), options['f']))
            if('w' in options): print(formatWorkersTable(getWorkers(data), options['f']))
            if('p' in options): print(formatPaymentsTable(getPayments(data), options['f']))

        if('c' in options): # repeat only c times if counter was set
            options['c'] -= 1
            if(options['c'] == 0): sys.exit(0)

        if('t' in options): # repeat every t seconds if timer was set
            sleep(options['t'])
            print("\n\n")
        else: sys.exit(0) # = execute only one time

def formatTotalStatsTable(totalStats, useFullFormat):
    table = ""
    if(useFullFormat):
        table += "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("PENDING BALANCE", totalStats['balance']+" XMR", "TOTAL HASHRATE", totalStats['hashrate'])
        table += "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("TOTAL PAID", totalStats['paid']+" XMR", "TOTAL HASHES", totalStats['hashes'])
        table += "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("LAST REWARD", totalStats['lastReward']+" XMR", "TOTAL EXPIRED", totalStats['expired'])
        table += "\t\t{:<15} | {:<29}\t\t{:<15} | {:<29}\n".format("LAST SHARE", totalStats['lastShare'], "TOTAL INNVALID", totalStats['invalid'])
    else:
        table += "\t{:<15} | {:<29}\n".format("PENDING BALANCE", totalStats['balance']+" XMR")
        table += "\t{:<15} | {:<29}\n".format("TOTAL PAID", totalStats['paid']+" XMR")
        table += "\t{:<15} | {:<29}\n".format("TOTAL HASHRATE", totalStats['hashrate']+" XMR")
        table += "\t{:<15} | {:<29}\n".format("LAST SHARE", totalStats['lastShare'])
    return table

def formatWorkersTable(workers, useFullFormat):
    table = ""
    if(useFullFormat):
        table += " {:^21}   {:^14}   {:^16}   {:^16}   {:^16}   {:^19}\n".format("WORKER ID", "HASHRATE", "HASHES", "EXPIRED", "INVALID", "LAST SHARE")
        table += " {:^21}   {:^14}   {:^16}   {:^16}   {:^16}   {:^19}\n".format("-"*21, "-"*14, "-"*16, "-"*16, "-"*16, "-"*19)
        for worker in workers:
            table += " {:<21}   {:^14}   {:>16}   {:>16}   {:>16}   {:^19}\n".format(" "+worker['workerId'], worker['hashrate'], worker['hashes']+" ", worker['expired']+" ", worker['invalid']+" ", worker['lastShare'])
    else:
        table += " {:^21}   {:^14}   {:^16}   {:^19}\n".format("WORKER ID", "HASHRATE", "HASHES", "LAST SHARE")
        table += " {:^21}   {:^14}   {:^16}   {:^19}\n".format("-"*21, "-"*14, "-"*16, "-"*19)
        for worker in workers:
            table += " {:<21}   {:^14}   {:>16}   {:^19}\n".format(" "+worker['workerId'], worker['hashrate'], worker['hashes']+" ", worker['lastShare'])
    return table

def formatPaymentsTable(payments, useFullFormat):
    table = ""
    if(useFullFormat):
        table += " {:^49}   {:^21}   {:^19}   {:^19}\n".format("TRANSACTION HASH", "AMOUNT", "DATE", "MIXIN")
        table += " {:^49}   {:^21}   {:^19}   {:^19}\n".format("-"*49, "-"*21, "-"*19, "-"*19)
        for payment in payments:
            table += " {:^49}   {:^21}   {:^19}   {:^19}\n".format(payment['hash'], payment['amount']+"€", payment['date'], payment['mixin'])
    else:
        table += " {:^21}   {:^19}   {:^19}\n".format("AMOUNT", "DATE", "MIXIN")
        table += " {:^21}   {:^19}   {:^19}\n".format("-"*21, "-"*19, "-"*19)
        for payment in payments:
            table += " {:^21}   {:^19}   {:^19}\n".format(payment['amount']+"€", payment['date'], payment['mixin'])
    return table

if __name__ == "__main__":

    if(len(sys.argv[1:]) > 0):  #if no argument was passed
        short_options = "ha:swpt:c:lf"
        long_options = ["help", "address=", "stats", "workers", "payments",
                        "time=", "counter=", "log", "full"]

        try:
            opts, _ = getopt.getopt(sys.argv[1:], short_options, long_options) # get env variables
        except getopt.GetoptError:
            print("Incorrect usage, use 'xmrpool-check.py -h' to see the correct one")
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                printHelp()
                break

            elif opt in ("-a", "--address"):

                try:
                    address = arg
                    options = getExtraOptions(opts)
                    while True:
                        plotData(options)

                except Exception as e:
                    print("[ERROR]", e)
                    sys.exit(1)
                break
            else: pass
    else:
        print("Incorrect usage. Use 'xmrpool-check.py -h' to see the correct one")
        sys.exit(2)