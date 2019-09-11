#!/usr/bin/env python

import subprocess
import optparse
import re


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


def check_result(interface, new_mac):
    # Catch the ifconfig result
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # Search for mac address in the ifconfig_result
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        # Get mac address
        mac_address = mac_address_search_result.group(0)
        if mac_address == new_mac:
            print("[+] MAC address has been changed from " + mac_address + " to " + new_mac)
        else:
            print("[-] No MAC address has been changed on " + interface)
    else:
        print("[-] There is no mac address to change on this interface : " + interface)


options = get_arguments()
mac_changer(options.interface, options.new_mac)
check_result(options.interface, options.new_mac)
