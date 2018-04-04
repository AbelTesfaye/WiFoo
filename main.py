#!/usr/bin/env python
import re
import subprocess
import tempfile
import os




def run_command_in_shell(command_to_run):
    with tempfile.TemporaryFile() as tempf:
        output=""
        proc = subprocess.Popen(command_to_run, stdout=tempf)
        proc.wait()
        tempf.seek(0)
        output+=tempf.read()
    return output

def get_interface_list(output_of_command):
    ## Takes output of the below command:
    ##   sudo airmon-ng

    ##output should be similar to this:
        
    '''

    Interface	Chipset		Driver

    wlp3s0		Intel 6205	iwlwifi - [phy0]
    wlp3s0		Intel 6205	iwlwifi - [phy0]
    wlp3s0		Intel 6205	iwlwifi - [phy0]
    wlp3s0		Intel 6205	iwlwifi - [phy0]


    '''
        
    text_to_parse = return_of_command


    text_to_parse = text_to_parse.splitlines()

    text_to_parse = filter(None, text_to_parse)

    wifi_cards = text_to_parse[1:]

    found_interface_list = list(str())
    for i in wifi_cards:
        found_interface_list.append(i.split('\t')[0])

    return found_interface_list


