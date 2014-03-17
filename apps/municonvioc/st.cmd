#/usr/bin/bash
system "python municonv.py"

epicsEnvSet("EPICS_HOSTNAME", "phyioc01")
epicsEnvSet("EPICS_IOCNAME", "municonv")
epicsEnvSet("CHF_UPDATE_DIR", "/cf-update")

dbLoadRecords("municonv.db")
iocInit()

system "python municonv.py false &"

dbl > ./$(EPICS_HOSTNAME).$(EPICS_IOCNAME).dbl
#dbl > ${CHF_UPDATE_DIR}/$(EPICS_HOSTNAME).$(EPICS_IOCNAME).dbl

