'''
Created on May 14, 2014

@author: dejan.dezman@cosylab.com
'''
import os
import sys

import unittest
import logging
import requests
import random
from utils.timer import Timer

import inspect
from requests import HTTPError

from idodspy.idodsclient import IDODSClient
from utils.profiler import *

__url = 'http://localhost:8000/id/device/'
__jsonheader = {'content-type': 'application/json', 'accept': 'application/json'}
client = IDODSClient(BaseURL=__url)


def idStatusHelper(inputStr):
    '''
    Clean ID status string and return correct int values

    :param inputStr: Input string
    :type inputStr: str

    :return: cleaned status

    '''

    if inputStr == "Y":
        return 0

    else:
        return 1


def idNoneHelper(inputStr, returnType=None):
    '''
    Clean ID input parameter

    :param inputStr: Input string
    :type inputStr: str

    :param returnType: Type of the returned data
    :type returnType: str

    :return: cleaned input

    '''

    # Strip input string of spaces
    inputStr = inputStr.strip()

    if inputStr == "None":
        return None

    else:

        if returnType is not None:

            if returnType == "float":
                return float(inputStr)

            else:
                return inputStr

        else:
            return inputStr


def saveInsertionDevices():
    '''
    Call client API to save devices and offline data
    '''

    # Map columns
    install_name = 0
    coordinate_center = 1
    project = 2
    beamline = 3
    beamline_desc = 4
    install_desc = 5
    inventory_name = 6
    down_corrector = 7
    up_corrector = 8
    length = 9
    gap_max = 10
    gap_min = 11
    gap_tolerance = 12
    phase1_max = 13
    phase1_min = 14
    phase2_max = 15
    phase2_min = 16
    phase3_max = 17
    phase3_min = 18
    phase4_max = 19
    phase4_min = 20
    phase_tolerance = 21
    k_max_circular = 22
    k_max_linear = 23
    phase_mode_a1 = 24
    phase_mode_a2 = 25
    phase_mode_p = 26
    type_name = 27
    type_desc = 28
    method = 29
    method_desc = 30
    data_desc = 31
    data_file_name = 32
    data_file_obsolete = 33
    gap = 34
    phase1 = 35
    phase2 = 36
    phase3 = 37
    phase4 = 38
    phase_mode = 39
    polar_mode = 40

    with Timer() as t:
        client.idodsInstall()
    print "=> elasped client.idodsInstall: %s s" % t.secs

    with Timer() as tt:
        with open('idods_data.csv') as f:
            index = 0

            for line in f:
                index += 1

                # Skip the first line
                if index == 1:
                    continue

                data = line.split(',')

                try:
                    with Timer() as t:
                        client.saveInsertionDevice(
                            install_name=idNoneHelper(data[install_name]),
                            coordinate_center=idNoneHelper(data[coordinate_center]),
                            project=idNoneHelper(data[project]),
                            beamline=idNoneHelper(data[beamline]),
                            beamline_desc=idNoneHelper(data[beamline_desc]),
                            install_desc=idNoneHelper(data[install_desc]),
                            inventory_name=idNoneHelper(data[inventory_name]),
                            down_corrector=idNoneHelper(data[down_corrector]),
                            up_corrector=idNoneHelper(data[up_corrector]),
                            length=idNoneHelper(data[length]),
                            gap_max=idNoneHelper(data[gap_max]),
                            gap_min=idNoneHelper(data[gap_min]),
                            gap_tolerance=idNoneHelper(data[gap_tolerance]),
                            phase1_max=idNoneHelper(data[phase1_max]),
                            phase1_min=idNoneHelper(data[phase1_min]),
                            phase2_max=idNoneHelper(data[phase2_max]),
                            phase2_min=idNoneHelper(data[phase2_min]),
                            phase3_max=idNoneHelper(data[phase3_max]),
                            phase3_min=idNoneHelper(data[phase3_min]),
                            phase4_max=idNoneHelper(data[phase4_max]),
                            phase4_min=idNoneHelper(data[phase4_min]),
                            phase_tolerance=idNoneHelper(data[phase_tolerance]),
                            k_max_circular=idNoneHelper(data[k_max_circular]),
                            k_max_linear=idNoneHelper(data[k_max_linear]),
                            phase_mode_a1=idNoneHelper(data[phase_mode_a1]),
                            phase_mode_a2=idNoneHelper(data[phase_mode_a2]),
                            phase_mode_p=idNoneHelper(data[phase_mode_p]),
                            type_name=idNoneHelper(data[type_name]),
                            type_desc=idNoneHelper(data[type_desc])
                        )
                    print "=> elasped client.saveInsertionDevice: %s s" % t.secs

                    with Timer() as t:
                        client.saveMethodAndOfflineData(
                            inventory_name=idNoneHelper(data[inventory_name]),
                            data_desc=idNoneHelper(data[data_desc]),
                            gap=idNoneHelper(data[gap]),
                            phase1=idNoneHelper(data[phase1]),
                            phase2=idNoneHelper(data[phase2]),
                            phase3=idNoneHelper(data[phase3]),
                            phase4=idNoneHelper(data[phase4]),
                            phase_mode=idNoneHelper(data[phase_mode]),
                            polar_mode=idNoneHelper(data[polar_mode]),
                            data_file_name=idNoneHelper(data[data_file_name]),
                            data_file_path='file.txt',
                            method=idNoneHelper(data[method]),
                            method_desc=idNoneHelper(data[method_desc]),
                            status=idStatusHelper(data[data_file_obsolete])
                        )
                    print "=> elasped client.saveMethodAndOfflineData: %s s" % t.secs

                except HTTPError as e:
                    print e

    print "=> elasped import: %s s" % tt.secs

@do_profile(follow=[client.testCall])
def timeTest():
    client.testCall()

import cProfile
cProfile.run('timeTest()')

saveInsertionDevices()
