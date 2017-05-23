import os

DEVICE_KEY = "devices"
ANSIBLE_COMPONENT_FILE = "ansibleFile"

ANSIBLE_HEAD_WORD = "---"
ANSBILE_INCLUDE_WORD = "- include: "

def setupAnsibleMain(rootPath, ansibleMainPath, components):
    if components == None:
        print "The components map should not be Null"
        return -1
    
    ansible_file_map = {}
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
            
            ansbileFilePath = rootPath + host[ANSIBLE_COMPONENT_FILE]
            ansible_file_map[hostKey] = ansbileFilePath
    
    buildAnsibleMainFile(ansibleMainPath, ansible_file_map)
    
def buildAnsibleMainFile(ansibleMainPath, ansible_file_map):
    if os.path.exists(ansibleMainPath):
        os.remove(ansibleMainPath)
    
    ansibleMainFile = os.open(ansibleMainPath, os.O_CREAT|os.O_RDWR)
    os.write(ansibleMainFile, ANSIBLE_HEAD_WORD + '\n')
    for ansibleFileKey in ansible_file_map.keys():
        ansibleFile = ansible_file_map[ansibleFileKey]
        os.write(ansibleMainFile, ANSBILE_INCLUDE_WORD + ansibleFile + '\n')