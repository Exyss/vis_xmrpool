#/usr/bin/python3
import urllib.request, json, sys, getopt

def getWalletData(address):

    xmrpoolAPI_url = "https://web.xmrpool.eu:8119/stats_address?address="+address+"&longpoll=false"
    request = urllib.request.urlopen(xmrpoolAPI_url)
    return json.loads(request.read().decode())

def getWorkers(data):

    workers = []
    for worker in data['perWorkerStats']:
        workers.append(formatWorkerData(worker))
    return workers

def formatWorkerData(worker):
    
    # define default values
    data = {'workerId': "unknown",
            'hashrate': "0.00 H",
            'hashes': "0",
            'lastShare': "unknown",
            'expired': "0",
            'invalid': "0"}

    # get data if found
    if ('workerId' in worker): data['workerId'] = worker['workerId']
    if ('hashrate' in worker): data['hashrate'] = worker['hashrate']
    if ('hashes' in worker): data['hashrate'] = worker['hashes']
    if ('lastShare' in worker): data['lastShare'] = worker['lastShare']
    if ('expired' in worker): data['expired'] = worker['expired']
    if ('invalid' in worker): data['invalid'] = worker['invalid']
    return data

"""
FOR FUTURE SUPPORT --- STATISTICS PAYMENTS STILL NOT IMPLEMENTED

def formatStatsData(stats):

def formatPaymentData(payment):
    time = payment['time'] if ('paymentId' in payment) else "unknown"
    hash = payment['hash'] if ('paymentId' in payment) else "unknown"
    amount = payment['amount'] if ('paymentId' in payment) else "unknown"
    mixin = payment['mixin'] if ('paymentId' in payment) else "unknown"
"""

def printHelp():
    print("----------------------------",
          "  xmrpool.eu Stat Visualizer",
          "           by Exyss",
          "",
          "DESCRIPTION",
          "  Fast visualization of all the statistics linked to a wallet used on xmrpool.eu",
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