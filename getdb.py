#!/usr/bin/python
"""doc string"""

import json
import logging
import urllib2

URL = 'http://the.open-budget.org.il/api/budget'


def get_url(url, fmt='json'):
    """gets url"""
    ret_url = url + '?o=' + fmt
    logging.info('Getting url: ' + ret_url)
    print 'Getting url: ' + ret_url
    retval = None
    try:
        retval = urllib2.urlopen(ret_url).read()
    except:
        # Usually a NotFound exception
        return '[]'
    # if len(d) > 10:
    #     fout = open(url[len(URL)+1:].replace('/', '_')+'.json', 'w')
    #     fout.write(unicode(d, 'utf8'))
    #     fout.close()
    return unicode(retval, 'utf8')

def get_years():
    """get years"""
    url = URL + '/00'
    raw_data = get_url(url)
    data = json.loads(raw_data)
    years = [str(yearly_data['year']) for yearly_data in data]
    years_str = ','.join(years)
    logging.info('Found years: ' + years_str)
    print 'Found years: ' + years_str
    return list(reversed(years))


def get_children(data):
    """get children"""
    return [child['code'] for child in data]


def get_code_data(code, year):
    """get code data"""
    url = URL + '/' + code + '/' + year
    raw_data = get_url(url)
    return json.loads(raw_data)


def recurse_children(code, year, data):
    """recurse children"""
    url = URL + '/' + code + '/' + year + '/kids'
    raw_data = get_url(url)
    new_data = json.loads(raw_data)
    children = get_children(new_data)
    child_data = {}
    for i, child in enumerate(children):
        child_data[child] = recurse_children(child, year, new_data[i])
        if len(child_data[child]) == 0:
            child_data[child] = new_data[i]
    data['children'] = child_data.values()
    return data

YEARS = get_years()
DATA = {}
# with open('outfile', 'w') as OUT:
# WRITER = None
for cur_year in YEARS:
    logging.info('At year ' + cur_year)
    print 'At year ' + str(cur_year)
    # DATA.append(get_code_data('0000', cur_year))
    # if len(DATA) == 1:
    #     WRITER = csv.DictWriter(OUT, DATA[0].keys(), extrasaction='ignore')
    #     WRITER.writeheader()
    d = recurse_children('0000', cur_year, {'code': '0000'})
    DATA[cur_year] = d
    with open(cur_year+'.json', 'w') as yearjson:
        json.dump(d, yearjson)
    # for v in d:
    #     WRITER.writerows(v)
with open('all.json', 'w') as outjson:
    json.dump(DATA, outjson)
