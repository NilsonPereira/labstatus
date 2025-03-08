#!../../bin/linux-x86_64/sts

## You may have to change sts to something else
## everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/sts.dbd"
sts_registerRecordDeviceDriver pdbbase

## Load record instances
#dbLoadRecords("db/xxx.db","user=nil")

cd "${TOP}/iocBoot/${IOC}"
dbLoadRecords("st.db")

iocInit

## Start any sequence programs
#seq sncxxx,"user=nil"
