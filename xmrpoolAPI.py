# Unofficial API module - last updated: 04.02.21
# Get the latest version here: https://github.com/Exyss/xmrpool-python-api
#
import urllib.request, json
import datetime

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
    for i, payment in enumerate(data['payments']):
        if i < len(data['payments'])-1:
            payments.append(_formatPaymentData(payment))
    return payments

def _formatTotalStatsData(totalStats):
    # define default values
    data = {'balance': "0",
            'lastReward': "0",
            'paid': "0",
            'hashrate': "0.00 H/s",
            'hashes': "0",
            'expired': "0",
            'invalid': "0",
            'lastShare': "unknown"}

    # get data if found
    if ('balance' in totalStats): data['balance'] = "{:.12f}".format(int(totalStats['balance'])/10**12)
    if ('last_reward' in totalStats): data['lastReward'] = "{:.12f}".format(int(totalStats['last_reward'])/10**12)
    if ('paid' in totalStats): data['paid'] = "{:.12f}".format(int(totalStats['paid'])/10**12)
    if ('hashrate' in totalStats): data['hashrate'] = totalStats['hashrate']+"/s"
    if ('hashes' in totalStats): data['hashes'] = f"{int(totalStats['hashes']):,}"
    if ('expired' in totalStats): data['expired'] = f"{int(totalStats['expired']):,}"
    if ('invalid' in totalStats): data['invalid'] = f"{int(totalStats['invalid']):,}"
    if ('lastShare' in totalStats): data['lastShare'] = _formatDatetime(int(totalStats['lastShare']))
    return data

def _formatWorkerData(worker):
    # define default values
    data = {'workerId': "unknown",
            'hashrate': "0.00 H/s",
            'hashes': "0",
            'lastShare': "unknown",
            'expired': "0",
            'invalid': "0"}

    # get data if found
    if ('workerId' in worker): data['workerId'] = worker['workerId']
    if ('hashrate' in worker): data['hashrate'] = worker['hashrate']+"/s"
    if ('hashes' in worker): data['hashes'] = f"{int(worker['hashes']):,}"
    if ('expired' in worker): data['expired'] = f"{int(worker['expired']):,}"
    if ('invalid' in worker): data['invalid'] = f"{int(worker['invalid']):,}"
    if ('lastShare' in worker): data['lastShare'] = _formatDatetime(int(worker['lastShare']))
    return data

def _formatPaymentData(payment):
    # define default values
    data = {'hash': "unknown",
            'amount': "0",
            'date': "unknown",
            'mixin': "unknown"}

    # get data if found
    bits = payment.split(':')
    if len(bits) == 4:
        data['hash'] = bits[0][:35]+"..."
        data['amount'] = "{:.12f}".format(int(bits[1])/10**12)
        data['date'] = _formatDatetime(int(bits[2]))
        data['mixin'] = bits[3]
    return data

def _formatDatetime(seconds):
    utc_date = datetime.datetime.fromtimestamp(seconds)
    local_date = utc_date.astimezone(datetime.datetime.now().tzname())
    return local_date.strftime("%d-%m-%y %H:%M:%S")