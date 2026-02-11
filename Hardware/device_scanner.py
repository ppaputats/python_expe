import usb.core
import usb.util

import serial.tools.list_ports
from ids_peak import ids_peak

def scan_usb_devices():
    devices = []
    for dev in usb.core.find(find_all=True):
        devices.append({
            "vendor_id": hex(dev.idVendor),
            "product_id": hex(dev.idProduct),
            "bus": dev.bus,
            "address": dev.address
        })
    return devices

def scan_ids_cameras():
    ids_peak.Library.Initialize()
    dm = ids_peak.DeviceManager.Instance()
    dm.Update()

    cams = []
    for dev in dm.Devices():
        cams.append({
            "name": dev.DisplayName(),
            "serial": dev.SerialNumber()
        })

    ids_peak.Library.Close()
    return cams

def scan_com_ports():
    ports = []
    for port in serial.tools.list_ports.comports():
        ports.append({
            "device": port.device,
            "description": port.description,
            "hwid": port.hwid
        })
    return ports

def scan_all_devices():
    return {
        "usb": scan_usb_devices(),
        "cameras": scan_ids_cameras(),
        "com_ports": scan_com_ports()
    }
