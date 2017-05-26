import os

DEVICE_KEY = "devices"
ANSIBLE_COMPONENT_FILE = "ansibleFile"

#Base service, should install first
ZOOKEEPER_KEY = "zookeeper"
KAFKA_KEY = "kafka"

ANSIBLE_HEAD_WORD = "---"
ANSBILE_INCLUDE_WORD = "- include: "

def setupAnsibleMain(rootPath, ansibleMainPath, components):
    if components == None:
        print "The components map should not be Null"
        return -1
    
    zookeeper_ansible_file_map = {}
    kafka_ansible_file_map = {}
    other_file_map = {}
    for componentKey in components.keys():
        component = components[componentKey]
        if component == None:
            print "The component " + componentKey + " should not be Null"
            continue
        
        ansible_file_map = None
        #Need to write the main.yaml in sort
        if(componentKey == ZOOKEEPER_KEY):
            ansible_file_map = zookeeper_ansible_file_map;
        elif(componentKey == KAFKA_KEY):
            ansible_file_map = kafka_ansible_file_map;
        else:
            ansible_file_map = other_file_map;
        
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
    
    buildAnsibleMainFileHeader(ansibleMainPath)
    buildAnsibleMainFile(ansibleMainPath, zookeeper_ansible_file_map)
    buildAnsibleMainFile(ansibleMainPath, kafka_ansible_file_map)
    buildAnsibleMainFile(ansibleMainPath, other_file_map)

def buildAnsibleMainFileHeader(ansibleMainPath):
    if os.path.exists(ansibleMainPath):
        os.remove(ansibleMainPath)
        
    ansibleMainFile = os.open(ansibleMainPath, os.O_CREAT|os.O_RDWR)
    os.write(ansibleMainFile, ANSIBLE_HEAD_WORD + '\n')
    os.close(ansibleMainFile)
    
    
def buildAnsibleMainFile(ansibleMainPath, ansible_file_map):
    
    #User os.O_APPEND to append the context to the file
    ansibleMainFile = os.open(ansibleMainPath, os.O_APPEND|os.O_RDWR)
    for ansibleFileKey in ansible_file_map.keys():
        ansibleFile = ansible_file_map[ansibleFileKey]
        os.write(ansibleMainFile, ANSBILE_INCLUDE_WORD + ansibleFile + '\n')
        
    os.close(ansibleMainFile)