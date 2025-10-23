#!/usr/bin/env python3

import sys
import math
'''
This script takes the number of hosts needed for each subnet
in the ip address of A,B, or C classes

'''

print("ENTER ip address: ")
ip_Address = input()


def detClass(val):
    '''
    This method is to determine the class
    '''
    if(val >= 0 and val <= 126):
        subnetMask = 8
        ip_class = 'A'
    if(val >= 128 and val <= 191):
        subnetMask = 16
        ip_class = 'B'
    if(val >= 192 and val <= 233):
        subnetMask = 24
        ip_class = 'C'
    return subnetMask, ip_class


def starting(array, mask):
    '''
    This method is to show the start of the process
    '''
    print(
        f"Designing subnets in the address:   {array[0]}.{array[1]}.{array[2]}.{array[3]}/{mask}\n")


def address(string):
    '''
    This method is to convert the ip string to a list of int
    '''
    oct1, oct2, oct3, oct4 = string.split(".")
    oct1 = int(oct1)
    oct2 = int(oct2)
    oct3 = int(oct3)
    oct4 = int(oct4)
    ip = []
    ip.extend([oct1, oct2, oct3, oct4])
    return ip


def userInput():
    '''
    This method is to get the user input
    '''
    list = []
    # to get user input
    for i in range(len(sys.argv)):
        if(i > 0):
            list.append(int(sys.argv[i]))

    # to solve example 19.10 

    # for i in range(64+128+128+1):
    #     if(i<64):
    #         list.append(250)
    #     elif(i>64 and i<192):
    #         list.append(124)
    #     else:
    #         list.append(60)
    return list


def mask(x):
    '''
    this method takes the number of hosts and returns the needed mask
    '''
    temp = math.ceil(math.log(x+2, 2))  # plus two --->netID and BCID
    y = 32-temp
    netSize = 2**temp
    return y, netSize, x


def formingIP(mask, size, address, x, hosts, ip_class):
    '''
    This method is to form netID, range of hosts, BCID
    '''
    if(size > 256):
        counter = int(size/256)
        size = 256
        ip_class = 'A'
    else:
        counter = int(1)
        ip_class = 'A'
    for i in range(counter):
        host_beg = address[3]+1
        host_end = address[3]+size-2
        bc_id = address[3]+size-1
        if(ip_class == 'A'):
            if(bc_id > 255):
                address[2] += 1
                address[3] = 0
                host_beg = address[3]+1
                host_end = address[3]+size-2
                bc_id = address[3]+size-1
            elif(address[2] > 255):
                address[1] += 1
                address[2] = 0
                address[3] = 0
                host_beg = address[3]+1
                host_end = address[3]+size-2
                bc_id = address[3]+size-1
            elif(address[1] > 255):
                print("This network has used all memebers of this ip address")
                exit(0)
            if(bc_id == 255 and i != 0):
                address[2] += 1
        elif(ip_class == 'B'):
            print(address[2])
            if(bc_id > 255):
                address[2] += 1
                address[3] = 0
                host_beg = address[3]+1
                host_end = address[3]+size-2
                bc_id = address[3]+size-1
            elif(address[2] > 255):
                print("This network has used all memebers of this ip address")
                exit(0)
            if(bc_id == 255 and i != 0):
                address[2] += 1
        elif(ip_class == 'C'):
            if(bc_id > 255):
                print("This network has used all memebers of this ip address")
                exit(0)
        if(i==0):
            print(f"Number of Hosts is: {hosts}")
        if(i==0):
            print(
            f"The netID:       {address[0]}.{address[1]}.{address[2]}.{address[3]}/{mask}\n")
        if(i==0):
            print(
            f"Host range: from {address[0]}.{address[1]}.{address[2]}.{host_beg}/{mask}\n")
        if(i==counter-1):
            print(
            f"            to   {address[0]}.{address[1]}.{address[2]}.{host_end}/{mask}\n")
        if(i==counter-1):
            print(
            f"The BC ID:       {address[0]}.{address[1]}.{address[2]}.{bc_id}/{mask}\n")


def netXX(net, ip, ip_class):
    '''
    This method is to iterate through all inputs
    '''
    print("-"*50)
    if(len(net) == 1):
        subnetMask, netSize, hosts = mask(net[0])
        formingIP(subnetMask, netSize, ip, net[0], hosts, ip_class)
        print('-'*50)
    else:
        for i in range(len(net)):
            subnetMask, netSize, hosts = mask(net[i])
            formingIP(subnetMask, netSize, ip, net[i], hosts, ip_class)
            ip[3] = netSize+ip[3]
            print('-'*50)

#############################################################################################################################################


# def main(array):
if __name__ == "__main__":
    '''
    This is the main method where all methods are invoked
    '''
    array = userInput()
    ip = address(ip_Address)
    subnetMask, ip_class = detClass(ip[0])
    starting(ip, subnetMask)
    netMembers = int(sum(array))+int((len(array)*2))
    array.sort(reverse=True)
    netXX(array, ip, ip_class)


# main(userInput())
