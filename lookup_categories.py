import httplib, urllib, csv, json, re, sys
from operator import itemgetter

conn = httplib.HTTPSConnection("data.mingle.io")
# expects a file of a CSV format, where product is the fifth column
# see https://github.com/cstuder/cumulizer/tree/master/_sampledata
reader = csv.reader(sys.stdin, delimiter=';')
for row in reader:
    # prepare the product name for better search
    item = row[5].replace("\"", "")
    item = re.sub('  .*$', '', item).strip()

    # compose a mingle.io query
    q = '{"query": "[a.category, a.product, fuzzy(upper(a.product), upper(\\"$1\\")) '
    q += '| a <- migipedia, ' 
    q += 'fuzzy(upper(a.product), upper(\\"$1\\")) > 0.40 && '
    q += 'a.lang == \\"de\\" ]", "limit": -1}'
    q = q.replace("$1", item)

    # execute the mingle.io query
    conn.request("POST", "", q)
    response = conn.getresponse()
    res = json.loads(response.read())
    conn.close()

    # sort the resposne and pick the best candidate
    body = res['body']
    body = sorted(body, key=itemgetter(2), reverse=True)
    if len(body) > 0:
        c = body[0][0].split("\\")
        p = body[0][1]
        conf = body[0][2]

        print [row[5], c[2], p, conf]
    else:
        print [row[5], "", "", 0.0]
