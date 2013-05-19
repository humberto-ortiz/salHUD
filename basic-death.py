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
import fileinput
from collections import defaultdict

bycounty = defaultdict(int)

for line in fileinput.input():
    fields = line.split(",")
    if fields[0] == "staymunnumunit":
        headers = fields
        unitidx = headers.index("ageunit")
        numbidx = headers.index("ageunitnumber")
        continue

    country = fields[headers.index("countryresidence")]
    municipio = fields[headers.index("placeresidence")]
    if country == "1":
        municipio = int(municipio)/4
        
        bycounty[municipio] += ypll(age(fields[unitidx], fields[numbidx]))
    

for county in bycounty.keys():
    print county, bycounty[county]
