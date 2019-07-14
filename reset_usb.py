""" Reset USB by searching for USB device ID "RTL2838"
this script was created partly out of https://github.com/mcarans/resetUSB/
much more possibilities for reset USB can find there"""

import os
import sys
from subprocess import Popen, PIPE
import fcntl
import logging

search_term = "RTL2838"


def create_usb_list():
    device_list = list()
    try:
        lsusb_out = Popen('lsusb -v', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, close_fds=True).stdout.read().strip().decode('utf-8')
        usb_devices = lsusb_out.split('%s%s' % (os.linesep, os.linesep))
        for device_categories in usb_devices:
            if not device_categories:
                continue
            categories = device_categories.split(os.linesep)
            device_stuff = categories[0].strip().split()
            bus = device_stuff[1]
            device = device_stuff[3][:-1]
            device_dict = {'bus': bus, 'device': device}
            device_info = ' '.join(device_stuff[6:])
            device_dict['description'] = device_info
            for category in categories:
                if not category:
                    continue
                categoryinfo = category.strip().split()
                if categoryinfo[0] == 'iManufacturer':
                    manufacturer_info = ' '.join(categoryinfo[2:])
                    device_dict['manufacturer'] = manufacturer_info
                if categoryinfo[0] == 'iProduct':
                    device_info = ' '.join(categoryinfo[2:])
                    device_dict['device'] = device_info
            path = '/dev/bus/usb/%s/%s' % (bus, device)
            device_dict['path'] = path
            device_list.append(device_dict)
    except Exception as ex:
        print('Failed to list USB devices! Error: %s' % ex)
        logging.error('Failed to list USB device!')
        sys.exit(-1)
    return device_list


def reset_usb_device(dev_path):
    USBDEVFS_RESET = 21780
    try:
        f = open(dev_path, 'w', os.O_WRONLY)
        fcntl.ioctl(f, USBDEVFS_RESET, 0)
        send_email.send_email_home("Successfull reset USB device!", "")
        print('Successfull reset USB device %s' % dev_path)
        logging.warning('Successfull reset USB device!')
        sys.exit(0)
    except Exception as ex:
        send_email.send_email_home("Failed to reset USB device", "")
        print('Failed to reset USB device! Error: %s' % ex)
        logging.error('Failed to reset USB device!')
        sys.exit(-1)


def reset_usb():
    usb_list = create_usb_list()
    for device in usb_list:
        text = '%s %s %s' % (device['description'], device['manufacturer'], device['device'])
        if search_term in text:
            reset_usb_device(device['path'])
    print('Failed to find USB device!')
    logging.error('Failed to find USB device!')
    sys.exit(-1)
