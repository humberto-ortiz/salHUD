# salHUD - a heads up display for public health information
# Copyright 2013 Humberto Ortiz-Zuazaga humberto.ortiz@upr.edu
# Released under the GNU General Public License v3
# http://www.fsf.org/gpl

# use R map of Puerto Rico
# http://blog.revolutionanalytics.com/2009/10/geographic-maps-in-r.html

# need sp
source("http://www.bioconductor.org/biocLite.R")
biocLite("sp")
library(sp)

# just the coastline
#load("PRI_adm0.RData")

# loads a "gadm" object

#spplot(gadm)

# municipalities
# http://www.filefactory.com/file/36b452f0rlrz/n/PRI_adm1_RData
load("PRI_adm1.RData")
names(gadm)
spplot(gadm, "ID_1")

gadm$NAME_1

# read csv file from institute of statistics
# http://www.estadisticas.gobierno.pr/iepr/
# http://www.estadisticas.gobierno.pr/iepr/Estadisticas/Basesdedatos/Salud.aspx#CDC_mort_ba

basic.death <- read.csv("basic-death-2008.txt")
colnames(basic.death)

# colum 28 is municinjury place of injury
# 004 Adjuntas
# 008 Aguada
# 012 Aguadilla
# 016 Aguas Buenas 
# 020 Aibonito
# 024 Añasco
# 028 Arecibo
# 032 Arroyo

# divide by 4 to get gadm unit.
# 346 means county not specified

basic.death[100:120,28]

# age at death
# ageunits
# 0 menos de 100
# 1 mas de 100
# 2 meses
# 3 Semanas
# 4 Días
# 5 Horas
# 6 Minutos
# X Edad desconocida

# ageunitnumber
# from 0 to 99 in the correct units
summary(basic.death["ageunit"])
summary(basic.death["ageunitnumber"])

## Jose Conde suggests
# 
# Years of Potential Life Lost (YPLL)
# 
# YPLL is a summary measure of premature mortality (early death). It represents the total number of years not lived by people who die before reaching a given age. Deaths among younger persons contribute more to the YPLL measure than deaths among older persons.
# YPLL is based on the number of deaths at each age up to some limit. For example, in the United States, the age limit is often placed at 75 (and sometimes the limit is set on 65 yeras old). People who die before age 75 are defined as having lost some potential years of life. YPLL has declined in the United States over the past decades. What about Puerto Rico?
# Although YPLL statistics have improved in the United States, they are often higher than those of comparable countries and even some less wealthy nations. For the 31 OECD countries for which recent data were available, the United States ranked 29th for females and 27th for males.
# 
# 
# So ....,  YPLL = Σ (75 - age at death)  for all deaths in a given time period. It can be calculated for all deaths, for specific causes of death, by gender, ... By the way, this might be a paper at least in the Puerto Rico Health Sciences Journal. I don't recall en update of the 1989 paper, I need to check.

# python basic-death.py basic-death-2008.txt > ypll.txt

ypll <- read.table("ypll.txt")

# plug data back into map
# careful, the numbers are off for 66+
gadm$ypll <- ypll$V2

# library(RColorBrewer)
# library(classInt)
# colours <- heat.colors(6)
# brks<-classIntervals(gadm$ypll, n=6, style="pretty")

spplot(gadm, "ypll")