#!/usr/bin/python
#
# Copyright (c) 2013 Brett Hutley <brett@hutley.net>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software screen-scrapes the myfitnesspal site, in order to
# store the diary food information in a Sqlite Database.

import os, sys
import urllib
from bs4 import BeautifulSoup
from tidylib import tidy_document
import datetime
import sqlite3
from ConfigParser import SafeConfigParser

def process_config(filename):
    conf = {}

    parser = SafeConfigParser()
    parser.read(filename)

    for section in parser.sections():
        for (name, value) in parser.items(section):
            #debug('%s => %s = %s' % (section, name, value))
            if not conf.has_key(section):
                conf[section] = {}
            conf[section][name] = value

    return conf

def get_url(url):
    html = urllib.urlopen(url).read()
    return html

date = datetime.date.today().isoformat()
if len(sys.argv) >= 2:
    date = sys.argv[1]

config = process_config(os.path.join(os.path.expanduser("~"), ".myfitnesspal.cfg"))

#Note: I am not doing any error checking here!!!
db_file = config['Database']['db_file']

base_url = config['MyFitnessPal']['base_url']
url = ("%s?date=%s" % (base_url, date, ))

html = get_url(url)
html, errors = tidy_document(html, options={'numeric-entities':1})
#print html

# Connect to the database
dbconn = sqlite3.connect(db_file)
c = dbconn.cursor()
c.execute('delete from food where dt = ?', [date, ])
dbconn.commit()

soup = BeautifulSoup(html)
divs = soup.find_all('div', { 'class' : 'food_container' })
if len(divs) > 0:
    div = divs[0]
    trs = div.find_all('tr')

    start_collecting = False
    headers = []
    for tr in trs:
        if tr.has_attr('class') and tr['class'][0] == unicode('meal_header'):
            start_collecting = True
            headers = []
            cols = tr.findAll('td')
            for col in cols:
                val = col.findAll(text=True)
                if len(val) > 0:
                    val = val[0].strip()
                    headers.append(val.encode('ascii', 'ignore'))
        elif tr.has_attr('class') and tr['class'][0] == unicode('bottom'):
            start_collecting = False
        elif start_collecting:
            cols = tr.findAll('td')
            values = []
            values.append(headers[0])
            for i in xrange(0, len(cols)):
                col = cols[i]
                val = col.findAll(text=True)
                if len(val) > 0:
                    val = val[0].strip()
                    val = val.encode('ascii', 'ignore')
                    if i >= 1:
                        val = val.replace(',', '') # remove commas from numbers
                    values.append(val)

            c.execute('insert into food(dt, meal, food, calories, carbs, fat, protein, sodium, sugar) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', [ date, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], ])
            dbconn.commit()

            
