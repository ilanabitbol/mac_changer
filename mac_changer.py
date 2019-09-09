#!/usr/bin/env python

import subprocess
import optparse


def get_arguments():
    # Parser creation
    parser = optparse.OptionParser()
    # Adding interface argument
    parser.add_option("-i", "--interface", dest="interface", help="Interface where changing MAC address")
    # Adding mac address argument
    parser.add_option("-m", "--mac", dest="new_mac", help="New mac address")
    # Handle user entry (options{eth0|11:22:33.44.55}, arguments{interface|mac})
    (loc_options, arguments) = parser.parse_args()
    if not loc_options.interface:
        parser.error("[-] Specify an interface, use --help for more info.")
    elif not loc_options.new_mac:
        parser.error("[-] Specify a MAC address, use --help for more info.")
    return loc_options

def mac_changer(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

options = get_arguments()
mac_changer(options.interface, options.new_mac)
