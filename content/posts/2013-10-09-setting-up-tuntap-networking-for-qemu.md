---
title: "Setting up Tun/Tap networking for a Qemu Image"
date: 2013-10-09T07:08:00.001Z
lastmod: 2026-01-13T23:34:40.391Z
tags:
  - tech
  - qemu
  - linux
aliases:
  - /2013/10/setting-up-tuntap-networking-for-qemu.html
---
Qemu is a very useful utility to play around with your code/application environment before you are ready to package it as a virtual appliance. Though there are various wikis available to help you setup networking between qemu guest and your host machine, I found that the steps required to setup TUN/TAP networking so that the guest is accessible from your extended network was either not accurate, or was not put in simple terms. So, here goes. Assuming that you are using Debian/Ubuntu as your host OS and you have qemu and necessary qemu-managers installed.
  * Add an additional interface (eth1) to your ubuntu host, assuming the ubuntu host is itself a virtual machine.
  * Create a bridge interface [ A bridge is used to connect two different network segements. In this case, your qemu guest OS with the rest of the network ].
  * To create a bridge, modify /etc/network/interfaces on Ubuntu host to create bridge and get dhcp address . This will also make eth0 come up without IP.

```
# Replace old eth0 config with br0
auto br0
# Use old eth0 config for br0, plus bridge stuff
iface br0 inet dhcp
    bridge_ports    eth0
    bridge_stp      off
    bridge_maxwait  0
    bridge_fd       0
```
  * Install uml-utilities to get a package called tunctl which helps in managing tunnel interfaces.

```
sudo apt-get install uml-utilities
```
  * Modify /etc/qemu-ifup :

```
set -x

switch=br0

if [ -n "$1" ];then
    /usr/bin/sudo /usr/sbin/tunctl -u `whoami` -t $1
    /usr/bin/sudo /sbin/ip link set $1 up
    sleep 0.5s
    /usr/bin/sudo /sbin/brctl addif $switch $1
    exit 0
else
    echo "Error: no interface specified"
    exit 1
fi
```
You can test this by running this script as :
```
cd /etc/
./qemu-ifup tap0
```
This will create a tap0 interface, and add br0 as a bridge to this.
  * Modify /etc/qemu-ifdown :

```
/usr/sbin/tunctl -d $1
```
This will delete the tap0 interface.
  * Start the image using the following command :

```
qemu-system-x86_64 -hda '/path/to/your/image/myimg.img' -m 256 -net nic,model=e1000, -net tap,ifname=tap0,script=/etc/qemu-ifup,downscript=/etc/qemu-ifdown
```
Couple of observations here :
```
-net nic,model=e1000, -net tap,ifname=tap0
```
Set the n/w interface model as e1000. For some reason, though my underlying nic card was getting detected , the corresponding drivers were not available for qemu to load. Setting it to generic e1000 solved the problem. Furthermore, the above command is setting networking to tap, with tap0 as the interface and providing script and downscript.
