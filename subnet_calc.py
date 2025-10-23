import math 
import re 

def subnet_mask_calc(hosts_number):
    """
    This method calculates the appropriate subnet masks
    for each subnet using VLSM
    """
    return 32 - math.ceil(math.log2(hosts_number+2)) # added two for NetID, and BCID

def bitwise_mask_calc(no_host_bits):
    """
    This method takes number of hosts bits as an input,
    and returns bitwise mask
    """
    hosts = [1, 2, 4, 8, 16, 32, 64, 128]
    return sum(hosts[no_host_bits:])

def R2R_ips(no_networks):
    """
    This method adds needed networks to link as many as needed sites.
    """
    if(no_networks==2):
        return [2 for i in range(no_networks-1)]
    elif(no_networks>2):
        return [2 for i in range(no_networks)]

def byte_modify(subnet_id_byte, broadcast_ip_byte, no_host_bits):
    """
    This method creates IPID, BCID, and range of usbale IPs 
    """
    subnet_id_byte = (subnet_id_byte & bitwise_mask_calc(no_host_bits)) + broadcast_ip_byte
    if(broadcast_ip_byte!=0):
        broadcast_ip_byte+=1 
        subnet_id_byte = broadcast_ip_byte 
    broadcast_ip_byte = broadcast_ip_byte + (2**no_host_bits) - 1 
    return subnet_id_byte, broadcast_ip_byte

def proper_inc(current_byte_netid, next_byte_netid, current_byte_bcid, next_byte_bcid):
    if(current_byte_bcid==255):
        current_byte_netid= 0
        current_byte_bcid = 0
        next_byte_netid  += 1
        next_byte_bcid   += 1
    return current_byte_netid, next_byte_netid, current_byte_bcid, next_byte_bcid

def assign_IP(subnet_id, broadcast_ip):
    """
    This method assigns subnets efficiently (minimizing wasted IP)
    """
    no_host_bits = 32-subnet_id[4]
    if(subnet_id[4] >= 24): # to modify the 4th byte 
        subnet_id[3], subnet_id[2], broadcast_ip[3], broadcast_ip[2] = proper_inc(subnet_id[3], subnet_id[2], broadcast_ip[3], broadcast_ip[2])
        subnet_id[3], broadcast_ip[3] = byte_modify(subnet_id[3],broadcast_ip[3], no_host_bits)
    elif(subnet_id[4] < 24 or subnet_id[4] >= 16): # to modify both 3rd and 4th 
        # Do oct 4 and 3 
        subnet_id[3], subnet_id[2], broadcast_ip[3], broadcast_ip[2] = proper_inc(subnet_id[3], subnet_id[2], broadcast_ip[3], broadcast_ip[2])
        subnet_id[2], subnet_id[1], broadcast_ip[2], broadcast_ip[1] = proper_inc(subnet_id[2], subnet_id[1], broadcast_ip[2], broadcast_ip[1])
        subnet_id[2], broadcast_ip[2] = byte_modify(subnet_id[2],broadcast_ip[2], (no_host_bits-8))
        subnet_id[3], broadcast_ip[3] = byte_modify(subnet_id[3],broadcast_ip[3], 8)
    elif(subnet_id[4] < 16 or subnet_id[4] >= 8): # to modify 2nd, 3rd, and 4th 
        # Do oct 4, 3, and 2
        subnet_id[3], subnet_id[2], broadcast_ip[3], broadcast_ip[2] = proper_inc(subnet_id[3], subnet_id[2], broadcast_ip[3], broadcast_ip[2])
        subnet_id[2], subnet_id[1], broadcast_ip[2], broadcast_ip[1] = proper_inc(subnet_id[2], subnet_id[1], broadcast_ip[2], broadcast_ip[1])
        subnet_id[1], subnet_id[0], broadcast_ip[1], broadcast_ip[0] = proper_inc(subnet_id[1], subnet_id[0], broadcast_ip[1], broadcast_ip[0])
        subnet_id[1], broadcast_ip[1] = byte_modify(subnet_id[1],broadcast_ip[1], (no_host_bits-16))
        subnet_id[2], broadcast_ip[2] = byte_modify(subnet_id[2],broadcast_ip[2], 8)
        subnet_id[3], broadcast_ip[3] = byte_modify(subnet_id[3],broadcast_ip[3], 8)
    else:
        # Do them all 
        print("Not yet")
        subnet_id[0], broadcast_ip[0] = byte_modify(subnet_id[0],broadcast_ip[0], no_host_bits-24)
        subnet_id[1], broadcast_ip[1] = byte_modify(subnet_id[1],broadcast_ip[1], 8)
        subnet_id[2], broadcast_ip[2] = byte_modify(subnet_id[2],broadcast_ip[2], 8)
        subnet_id[3], broadcast_ip[3] = byte_modify(subnet_id[3],broadcast_ip[3], 8)

    return subnet_id, broadcast_ip


def display_output(subnet_id, broadcast_ip, file):
    """
    This method formats the output 
    """
    file.write(f"\nsubnet_idnet: {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}/{subnet_id[4]}\n")
    print(f"\nsubnet_idnet: {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}/{subnet_id[4]}")
    file.write(f"Mask: {subnet_id[4]}\n")
    print(f"Mask: {subnet_id[4]}")
    file.write(f"Range: {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]+1}/{subnet_id[4]} -- {broadcast_ip[0]}.{broadcast_ip[1]}.{broadcast_ip[2]}.{broadcast_ip[3]-1}/{broadcast_ip[4]}\n")
    print(f"Range: {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]+1}/{subnet_id[4]} -- {broadcast_ip[0]}.{broadcast_ip[1]}.{broadcast_ip[2]}.{broadcast_ip[3]-1}/{broadcast_ip[4]}")
    file.write(f"Broadcast address: {broadcast_ip[0]}.{broadcast_ip[1]}.{broadcast_ip[2]}.{broadcast_ip[3]}/{broadcast_ip[4]}\n")
    print(f"Broadcast address: {broadcast_ip[0]}.{broadcast_ip[1]}.{broadcast_ip[2]}.{broadcast_ip[3]}/{broadcast_ip[4]}")
    file.write(f"Usable hosts: {(2**(32-subnet_id[4]))-2}\n")
    print(f"Usable hosts: {(2**(32-subnet_id[4]))-2}")
    file.write("\n----------------------------------------------------\n")
    print("\n----------------------------------------------------\n")

def validate_input(ip_address, subnet_chunks):
    if any(i > 255 for i in ip_address):
        raise ValueError("Input cannot be greater than 255!")
    elif any(i < 0 for i in ip_address):
        raise ValueError("Input cannot be negative!")
    elif any(i < 0 for i in subnet_chunks):
        raise ValueError("SERIOUSLY!!! You cannot have a negative number of people. Only Zombies don't count, but they don't use computers!")
    elif (ip_address[4]> 32):
        raise ValueError("Subnet mask cannot be greater than 32!")
    elif (len(ip_address) != 5):
        raise ValueError("Wrong input!")

if __name__ == "__main__":
    """
    This is the main method
    """
    ip_address = list(map(int, re.sub(r'[.,/\s+]',' ', input("Enter base network (CIDR): ")).strip().split(' ')))
    subnet_chunks = list(map(int, input("Enter required hosts per subnet (comma-separated): ").split(', ')))
    # validate input
    validate_input(ip_address, subnet_chunks) 


    with open("subnet_report.txt", "w") as file:
        file.write("Hey, lazy engineer! Go learn how to subnet by yourself! Don't use this tool again!\n This is a detailed report of your subneting design!\n")
        file.write("\n----------------------------------------------------\n")
        subnet_chunks.sort(reverse=True)
        routing_networks = R2R_ips(len(subnet_chunks))
        subnet_chunks.extend(routing_networks)
        subnet_id = ip_address.copy()
        broadcast_ip = ip_address.copy()
        visualization_ips = []
        for i in subnet_chunks:
            subnet_id[4] = subnet_mask_calc(i)
            broadcast_ip[4] = subnet_mask_calc(i)
            subnet_id, broadcast_ip = assign_IP(subnet_id, broadcast_ip)
            visualization_ips.append(subnet_id)
            display_output(subnet_id, broadcast_ip, file)
