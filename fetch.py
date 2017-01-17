from __future__ import division
import requests
import json

def get_transactions(address, offset=0):
    url = 'https://blockchain.info/address/%s?format=json&limit=50&offset=%d' % (address, offset)
    request = requests.get(url)
    return request.json()

btc_address = '1HB5XMLmzFVj8ALj6mfBsbifRoD4miY36v'
total_transactions = get_transactions(btc_address)['n_tx']

processed = 0
_next = 0
batch_size = 50

with open('txs.json', 'w+') as f:
    f.write("[\n")
    while processed < total_transactions:
        body = get_transactions(btc_address, _next)
        txs = body['txs']
        processed += len(txs)
        trailing = ", \n" if processed < total_transactions else "\n"
        f.write(json.dumps(txs) + trailing)
        print 'processed %d (%d%%)' % (
            processed, processed / total_transactions * 100)
        _next += batch_size
    f.write("]\n")
