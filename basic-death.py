# basic-death.py - Parse basic death data from instituto de estadisticas
# Copyright 2013 - Humberto Ortiz-Zuazaga
# GPL v3

# age at death
# ageunits
# 0 menos de 100
# 1 mas de 100
# 2 meses
# 3 Semanas
# 4 Dias
# 5 Horas
# 6 Minutos
# X Edad desconocida

# ageunitnumber
# from 0 to 99 in the correct units

def age(units, number):
    #print [units, number]
    if number == ' ':
        return None
    
    if units == "0":
        retval = int(number)
    elif units == "1":
        retval = 100 + int(number)
    elif units == "2":
        retval = int(number) / 12.0
    elif units == "3":
        retval = int(number) / 52.0
    elif units == "4":
        retval = int(number) / 365.0
    elif units == "5":
        retval = int(number) / (365*24)
    elif units == "6":
        retval = int(number) / (365*24*60)
    else:
        retval = None
    return retval

def ypll(years):
    
    if years >= 75 or years == None:
        return 0
    else:
        return 75 - years

# main
import re
import fileinput
from collections import defaultdict

import csv

munimap = {}

with open("municipios-fipsV2.csv","r") as municipios:
    munireader = csv.reader(municipios)
    for row in munireader:
        munimap[ row[2]] = row[0]
        
        
bycounty = defaultdict(int)
bydeath = defaultdict(lambda : defaultdict(int))

causes = ["cardio", "tumor", "diabetes", "alzheimer", "cerebrovascular", "respiratory", "accident", "nefritis", "homicide", "pneumonia"]

# Use named groups, raw triple quoted strings, and verbose syntax to
# split across multiple lines.
reg_exp = re.compile(r"""(?P<cardio>I(0[0-9]|11|13|[234][0-9]|5[0-1]))|
(?P<tumor>C([0-8][0-9]|9[0-7]))|
(?P<diabetes>E(1[0-4]))|
(?P<alzheimer>G30)|
(?P<cerebrovascular>I(6[0-9]))|
(?P<respiratory>J(4[0-7]))|
(?P<accident>V(0[1-9]|[1-9][0-9])|W([0-9][0-9])|X([0-5][0-9]))|
(?P<nefritis>N(0[0-7]|1[7-9]|2[5-7]))|
(?P<homicide>X(8[5-9]|9[0-9])|Y(0[0-9]|87\.1)|U(0[12]))|
(?P<pneumonia>J(09|1[0-9]|2[01]))""", re.VERBOSE)

for line in fileinput.input():
    fields = line.split(",")
    if fields[0] == "staymunnumunit":
        headers = fields
        unitidx = headers.index("ageunit")
        numbidx = headers.index("ageunitnumber")
        continue
    
    icd = fields[headers.index("cod_icd10")]
    #print icd, 
    m = reg_exp.search(icd)
    if m:
	cause = m.lastgroup # prints the name of the group that matched
    else:
        cause = "other"

    country = fields[headers.index("countryresidence")]
    municipio = fields[headers.index("placeresidence")]
    if country == "1":
        municipio = munimap[municipio]
        
        bycounty[municipio] += ypll(age(fields[unitidx], fields[numbidx]))
        bydeath[municipio][cause] += ypll(age(fields[unitidx], fields[numbidx]))
    

import json

data = []
for county in bycounty.keys():
    data.append(bydeath[county])
    data[-1]["fips"] = county
    data[-1]["ypll"] = bycounty[county]
    
print json.dumps(data)

#print "# municipio total",

#for cause in  causes:
#    print cause,
#
#print
#
#for county in bycounty.keys():
#    print county, bycounty[county],
#
#    for cause in causes:
#	print bydeath[county][cause],
#
#    print
