#/usr/bin/bash

system "python lattice.py"
epicsEnvSet("EPICS_CA_MAX_ARRAY_BYTES", "200000")
epicsEnvSet("EPICS_HOSTNAME", "phyioc01")
epicsEnvSet("EPICS_IOCNAME", "lattice")

epicsEnvSet("CHF_UPDATE_DIR", "/cf-update")

dbLoadRecords("design.db")
dbLoadRecords("livesp.db")
dbLoadRecords("liverb.db")
iocInit()

system "python lattice.py false &"

dbl > ./$(EPICS_HOSTNAME).$(EPICS_IOCNAME).dbl
#dbl > ${CHF_UPDATE_DIR}/$(EPICS_HOSTNAME).$(EPICS_IOCNAME).dbl

