import os

DEVICE_KEY = "devices"
ANSIBLE_COMPONENT_FILE = "ansibleFile"

#Base service, should install first
ZOOKEEPER_KEY = "zookeeper"
KAFKA_KEY = "kafka"

ANSIBLE_HEAD_WORD = "---"
ANSBILE_INCLUDE_WORD = "- include: "

COMMON_PRE_STEP_KEY = "preStep"
COMMON_POST_STEP_KEY = "postStep"
COMMON_ANSIBLE_FILE = "ansibleFile"

def setupAnsibleMain(rootPath, ansibleMainPath, components, commons):
    
    buildAnsibleMainFileHeader(ansibleMainPath)
    setupAnsibleCommonsPreStep(rootPath, ansibleMainPath, commons)
    setupAnsibleComponents(rootPath, ansibleMainPath, components)
    setupAnsibleCommonsPostStep(rootPath, ansibleMainPath, commons)
    
def setupAnsibleCommonsPreStep(rootPath, ansibleMainPath, commons):
    
    if commons == None:
        print "No common service, just return"
        return
    
    ansible_file_map = {}
    
    for commonServiceKey in commons.keys():
        commonService = commons[commonServiceKey]
        if commonService == None:
            print "commonService should not be null " + commonServiceKey
            continue
        
        if not commonService.has_key(COMMON_PRE_STEP_KEY):
            print "service do not contain the pre step " + commonServiceKey
            continue
        
        preStep = commonService[COMMON_PRE_STEP_KEY]
        if preStep == None:
            print "preStep should not be null"
            continue
        
        ansible_file_map[commonServiceKey] = rootPath + preStep[COMMON_ANSIBLE_FILE]
        
    buildAnsibleMainFile(ansibleMainPath, ansible_file_map)
    
def setupAnsibleComponents(rootPath, ansibleMainPath, components):
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
    
    buildAnsibleMainFile(ansibleMainPath, zookeeper_ansible_file_map)
    buildAnsibleMainFile(ansibleMainPath, kafka_ansible_file_map)
    buildAnsibleMainFile(ansibleMainPath, other_file_map)

def setupAnsibleCommonsPostStep(rootPath, ansibleMainPath, commons):

    if commons == None:
        print "No common service, just return"
        return
    
    ansible_file_map = {}
    
    for commonServiceKey in commons.keys():
        commonService = commons[commonServiceKey]
        if commonService == None:
            print "commonService should not be null " + commonServiceKey
            continue
        
        if not commonService.has_key(COMMON_POST_STEP_KEY):
            print "service do not contain the post step " + commonServiceKey
            continue
        
        postStep = commonService[COMMON_POST_STEP_KEY]
        if postStep == None:
            print "postStep should not be null"
            continue
        
        ansible_file_map[commonServiceKey] = rootPath + postStep[COMMON_ANSIBLE_FILE]
        
    buildAnsibleMainFile(ansibleMainPath, ansible_file_map)

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