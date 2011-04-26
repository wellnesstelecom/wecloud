#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# author: javi santana


import os
import json
from os.path import join
from fabric.api import run, cd, env, put

setup_file = """#!/bin/sh
echo "auto eth1" >> /etc/network/interfaces
echo "iface eth1 inet static" >> /etc/network/interfaces
echo "    address %s" >> /etc/network/interfaces
echo "    netmask 255.255.255.0" >> /etc/network/interfaces
echo "    gateway 10.200.6.2" >> /etc/network/interfaces
echo "    metric 0" >> /etc/network/interfaces

"""

def generate_setup(where, ip):
    open('setup.sh','w').write(setup_file % ip)

def vagrant(cmd):
    run("vagrant " + cmd)

def create_vm(name, ip):
    """ create a new vm with spcified ip attached to host eth card """
    home = os.getenv("HOME")
    run("mkdir %s" % name)
    with cd(name):
        vagrant("init")
        # set config
        put("Vagrantfile", ".")
        generate_setup(join(home,name), ip)
        put("setup.sh", ".")
        # init vm and then halt to setup host network
        vagrant("up")
        vagrant("halt")
        # .vagrant contains json with virtualbox vms uuids
        json_text = run("cat .vagrant")
        vm_uuid = json.loads(json_text)['active']['default']
        # change network mode
        run("vboxmanage modifyvm %s --nic2 bridged --bridgeadapter2 eth0" % vm_uuid)


def cloud_machine():
    env.hosts = ['127.0.0.1']
    env.user = ''
    env.password = ''






