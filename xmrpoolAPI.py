# Unofficial API module - last updated: 02.02.21
# Get the latest version here: https://github.com/Exyss/xmrpool-api.git
#
import urllib.request, json
from time import strftime
from time import gmtime

strftime("%H:%M:%S", gmtime(666))

def getWalletData(address):

    xmrpoolAPI_url = "https://web.xmrpool.eu:8119/stats_address?address="+address+"&longpoll=false"
    request = urllib.request.urlopen(xmrpoolAPI_url)
    return json.loads(request.read().decode())

def getWorkers(data):

    workers = []
    for worker in data['perWorkerStats']:
        workers.append(_formatWorkerData(worker))
    return workers

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
    if ('hashes' in worker): data['hashes'] = worker['hashes']
    if ('lastShare' in worker): data['lastShare'] = strftime("%d-%m-%y %H:%M:%S", gmtime(int(worker['lastShare'])))
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