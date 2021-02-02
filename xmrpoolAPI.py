# Unofficial API module - last updated: 02.02.21
# Get the latest version here: https://github.com/Exyss/xmrpool-api.git
#
import urllib.request, json
from time import strftime
from time import gmtime

def getWalletData(address):
    xmrpoolAPI_url = "https://web.xmrpool.eu:8119/stats_address?address="+address+"&longpoll=false"
    request = urllib.request.urlopen(xmrpoolAPI_url)
    return json.loads(request.read().decode())

def getTotalStats(data):
    totalStats = data['stats']
    return _formatTotalStatsData(totalStats)

def getWorkers(data):
    workers = []
    for worker in data['perWorkerStats']:
        workers.append(_formatWorkerData(worker))
    return workers

def getPayments(data):
    payments = []
    for payment in data['payments']:
        payments.append(_formatPaymentData(payment))
    return payments

def _formatTotalStatsData(totalStats):
    # define default values
    data = {'balance': "0",
            'lastReward': "0",
            'paid': "0",
            'hashrate': "0.00 H",
            'hashes': "0",
            'expired': "0",
            'invalid': "0",
            'lastShare': "unknown"}

    # get data if found
    if ('balance' in totalStats): data['balance'] = "{:.12f}".format(int(totalStats['balance'])/10**12)
    if ('last_reward' in totalStats): data['lastReward'] = "{:.12f}".format(int(totalStats['last_reward'])/10**12)
    if ('paid' in totalStats): data['paid'] = "{:.12f}".format(int(totalStats['paid'])/10**12)
    if ('hashrate' in totalStats): data['hashrate'] = totalStats['hashrate']
    if ('hashes' in totalStats): data['hashes'] = f"{int(totalStats['hashes']):,}"
    if ('expired' in totalStats): data['expired'] = f"{int(totalStats['expired']):,}"
    if ('invalid' in totalStats): data['invalid'] = f"{int(totalStats['invalid']):,}"
    if ('lastShare' in totalStats): data['lastShare'] = strftime("%d-%m-%y %H:%M:%S", gmtime(int(totalStats['lastShare'])))
    return data

def _formatWorkerData(worker):
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
    if ('hashes' in worker): data['hashes'] = f"{int(worker['hashes']):,}"
    if ('expired' in worker): data['expired'] = f"{int(worker['expired']):,}"
    if ('invalid' in worker): data['invalid'] = f"{int(worker['invalid']):,}"
    if ('lastShare' in worker): data['lastShare'] = strftime("%d-%m-%y %H:%M:%S", gmtime(int(worker['lastShare'])))
    return data

def _formatPaymentData(payment):
    # define default values
    data = {'hash': "unknown",
            'amount': "0",
            'date': "unknown",
            'mixin': "unknown"}

    # get data if found
    if ('amount' in payment): data['amount'] = payment['amount']
    if ('hash' in payment): data['hash'] = payment['hash']
    if ('time' in payment): data['date'] = strftime("%d-%m-%y %H:%M:%S", gmtime(int(payment['time'])))
    if ('mixin' in payment): data['mixin'] = payment['mixin']
    return data