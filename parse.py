import json
import csv

def maybe(key, map):
    return map[key] if key in map else 'NA'

def parse(items):
    for item in items:
        inputs = item['inputs']
        hash = item['hash']
        tx_index = item['tx_index']
        relayed_by = item['relayed_by']
        time = item['time']
        for i in inputs:
            if 'prev_out' not in i: continue
            out = i['prev_out']
            addr_tag = maybe('addr_tag', out)
            addr_tag_link = maybe('addr_tag_link', out)
            addr = out['addr']
            value = out['value']
            yield(tx_index, hash, relayed_by, time, addr, value, addr_tag, addr_tag_link)

with open('txs.json', 'r') as f:
    data = json.loads(f.read())
    flat_data = [item for sublist in data for item in sublist]
    parsed = parse(flat_data)

with open('txs.csv', 'wb+') as csvfile:
    fieldnames = ['tx_index', 'hash', 'relayed_by', 'time', 'addr', 'value', 'addr_tag', 'addr_tag_link']
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(fieldnames)
    for (tx, hsh, relayed, time, addr, value, addr_tag, addr_tag_link) in parsed:
        writer.writerow([tx, hsh, relayed, time, addr, value, addr_tag, addr_tag_link])

