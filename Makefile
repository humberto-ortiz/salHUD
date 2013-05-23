all: ypll-2008.png

ypll-2008.png: salHUD.R PRI_adm1.RData ypll.txt
	R CMD BATCH salHUD.R

PRI_adm1.RData:
	wget http://www.filefactory.com/file/36b452f0rlrz/n/PRI_adm1_RData
	mv PRI_adm1_RData PRI_adm1.RData

ypll.txt: basic-death-2008.txt basic-death.py
	python basic-death.py basic-death-2008.txt > ypll.txt
