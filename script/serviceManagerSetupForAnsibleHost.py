import os

DEVICE_KEY = "devices"
ANSIBLE_HOST_NAME_KEY = "name"
ANSIBLE_HOST_USER_KEY = "user"
ANSIBLE_HOST_PASSWORD_KEY = "password"
ANSIBLE_HOST_IP_KEY = "ip"

ANSIBLE_HOST_USER_TAG = "ansible_ssh_user"
ANSIBLE_HOST_PASSWORD_TAG = "ansible_ssh_pass"
ANSIBLE_HOST_SUDO_PASSWORD_TAG = "ansible_sudo_pass"

def setupAnsibleHost(ansibleHostPath, components):
    if components == None:
        print "The components map should not be Null"
        return -1
    
    host_map = {}
    for componentKey in components.keys():
        component = components[componentKey]
        if component == None:
            print "The component " + componentKey + " should not be Null"
            continue
        
        devices = component[DEVICE_KEY]
        if devices == None:
            print "The device " + componentKey + " should not be Null"
            continue
        
        for hostKey in devices.keys():
            host = devices[hostKey]
            if host == None:
                print "The host " + hostKey + " should not be Null"
                continue
            
            host_info = {}
            host_info[ANSIBLE_HOST_NAME_KEY] = host[ANSIBLE_HOST_NAME_KEY]
            host_info[ANSIBLE_HOST_USER_KEY] = host[ANSIBLE_HOST_USER_KEY]
            host_info[ANSIBLE_HOST_PASSWORD_KEY] = host[ANSIBLE_HOST_PASSWORD_KEY]
            host_info[ANSIBLE_HOST_IP_KEY] = host[ANSIBLE_HOST_IP_KEY]
            host_map[hostKey] = host_info
    
    buildAnsibleHost(ansibleHostPath, host_map)
    
def buildAnsibleHost(ansibleHostPath, host_map):
    if os.path.exists(ansibleHostPath):
        os.remove(ansibleHostPath)
        
    ansibleHostFile = os.open(ansibleHostPath, os.O_CREAT|os.O_RDWR)
    for hostKey in host_map.keys():
        hostHeader = "[" + hostKey + "]" + "\n"
        os.write(ansibleHostFile, hostHeader)
        host = host_map[hostKey]
        hostBody = host[ANSIBLE_HOST_IP_KEY] + " " + ANSIBLE_HOST_USER_TAG + "=" + host[ANSIBLE_HOST_USER_KEY] + \
                                               " " + ANSIBLE_HOST_PASSWORD_TAG + "=" + host[ANSIBLE_HOST_PASSWORD_KEY] + \
                                               " " + ANSIBLE_HOST_SUDO_PASSWORD_TAG + "=" + host[ANSIBLE_HOST_PASSWORD_KEY] + "\n"
        os.write(ansibleHostFile, hostBody)
    
    
    
       
