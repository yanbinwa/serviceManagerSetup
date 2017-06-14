import os

DEVICE_KEY = "devices"
ANSIBLE_HOST_NAME_KEY = "name"
ANSIBLE_HOST_USER_KEY = "user"
ANSIBLE_HOST_PASSWORD_KEY = "password"
ANSIBLE_HOST_IP_KEY = "ip"

ANSIBLE_HOST_USER_TAG = "ansible_ssh_user"
ANSIBLE_HOST_PASSWORD_TAG = "ansible_ssh_pass"
ANSIBLE_HOST_SUDO_PASSWORD_TAG = "ansible_sudo_pass"

ANSIBLE_HOST_SERVICEGROUP_TAG = "serviceGroup"

def setupAnsibleHost(ansibleHostPath, components, commons):
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
    
    setupAnsibleCommonHost(ansibleHostPath, components, commons, host_map)
    
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
        
    os.close(ansibleHostFile)


def setupAnsibleCommonHost(ansibleHostPath, components, commons, host_map):
    if commons == None:
        print "No commons service need, just return"
        return
    
    for commonServiceKey in commons.keys():
        commonService = commons[commonServiceKey]
        if commonService == None:
            print "commonService should not be empty " + commonServiceKey
            continue
        
        serviceGroupListStr = commonService[ANSIBLE_HOST_SERVICEGROUP_TAG]
        if serviceGroupListStr == None:
            print "serviceGroupListStr should not be empty" + commonServiceKey
            continue
        
        common_host_map = {}
        serviceGroupList = serviceGroupListStr.split(',')
        for serviceGourp in serviceGroupList:
            component = components[serviceGourp]
            if component == None:
                print "components should contain the component " + serviceGourp
                continue
            devices = component[DEVICE_KEY]
            if devices == None:
                print "The device " + serviceGourp + " should not be Null"
                continue
            
            for hostKey in devices.keys():
                host = devices[hostKey]
                if host == None:
                    print "The host " + hostKey + " should not be Null"
                    continue
                common_host_map[hostKey] = host_map[hostKey]
        
        
    buildAnsibleCommonHost(ansibleHostPath, commonServiceKey, common_host_map)       
    
def buildAnsibleCommonHost(ansibleHostPath, commonHostName, common_host_map):
    ansibleHostFile = os.open(ansibleHostPath, os.O_APPEND|os.O_RDWR)
    hostHeader = "[" + commonHostName + "]" + "\n"
    os.write(ansibleHostFile, hostHeader)
    for hostKey in common_host_map.keys():
        host = common_host_map[hostKey]
        hostBody = host[ANSIBLE_HOST_IP_KEY] + " " + ANSIBLE_HOST_USER_TAG + "=" + host[ANSIBLE_HOST_USER_KEY] + \
                                               " " + ANSIBLE_HOST_PASSWORD_TAG + "=" + host[ANSIBLE_HOST_PASSWORD_KEY] + \
                                               " " + ANSIBLE_HOST_SUDO_PASSWORD_TAG + "=" + host[ANSIBLE_HOST_PASSWORD_KEY] + "\n"
        os.write(ansibleHostFile, hostBody)
        
    os.close(ansibleHostFile)
    
    
       
