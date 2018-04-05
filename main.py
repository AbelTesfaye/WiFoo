#!/usr/bin/env python
import re
import subprocess
import tempfile
import os




def run_command_in_shell(command_to_run,max_timeout_in_sec):
    with tempfile.TemporaryFile() as tempf:
        output=""        
        proc = subprocess.Popen(command_to_run, stdout=tempf,stderr=tempf,shell=True)
        try:
            process_return = proc.wait(timeout=max_timeout_in_sec)
        except subprocess.TimeoutExpired as e:
            pass
 
        tempf.seek(0)
        output+=str(tempf.read().decode("utf-8"))
            
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

def get_monitor_mode_enabled_interface_name(output_of_command):
    ## Takes output of the below command:
    ##  sudo airmon-ng start wlp3s0

    ##output should be similar to this:
        
    '''


    Found 5 processes that could cause trouble.
    If airodump-ng, aireplay-ng or airtun-ng stops working after
    a short period of time, you may want to kill (some of) them!

    PID	Name
    879	NetworkManager
    882	avahi-daemon
    940	avahi-daemon
    1032	wpa_supplicant
    1318	dhclient
    Process with PID 1318 (dhclient) is running on interface wlp3s0


    Interface	Chipset		Driver

    wlp3s0		Intel 6205	iwlwifi - [phy0]
				(monitor mode enabled on mon0)


    '''
    text_to_parse=output_of_command
    match = re.search("\(monitor mode enabled on (.*)\)", text_to_parse)
    if match:
        found_monitor_mode_interface = match.group(1)

        return found_monitor_mode_interface

    
    return None
    


def get_devices_on_nearby_networks(output_of_command):
    ## Takes output of the below command:
    ##  sudo airodump-ng mon0

    ##output should be similar to this:

    text_to_parse = '''










































     CH  8 ][ Elapsed: 4 s ][ 2018-04-05 20:08                                         
                                                                                                                 
     BSSID              PWR  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID
                                                                                                                 
     88:DC:96:0D:FC:60  -73       48       26    1   6  54e. WPA2 CCMP   PSK  DODO                               
                                                                                                                 
     BSSID              STATION            PWR   Rate    Lost    Frames  Probe                                   
                                                                                                                 
     88:DC:96:0D:FC:60  80:7A:BF:BB:D8:16  -51    0e- 1      1       27                                           
     88:DC:96:0D:FC:60  84:B5:41:50:78:D2  -84    0 - 1      0        1                                           

    '''

    match = re.search(r"BSSID\s*PWR\s*Beacons\s*#Data,\s*#/s\s*CH\s*MB\s*ENC\s*CIPHER\s*AUTH\s*ESSID(.*)BSSID\s*STATION\s*PWR\s*Rate\s*Lost\s*Frames\s*Probe", text_to_parse,re.MULTILINE|re.DOTALL)
    if match:
        print(match.groups())




get_devices_on_nearby_networks("")







    


        
