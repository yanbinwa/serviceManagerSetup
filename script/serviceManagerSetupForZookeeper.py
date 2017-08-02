import os
import serviceManagerSetupConstants

ZOOKEEPER_DATA_PATH_KEY = "data_dir"
ZOOKEEPER_DATALOG_PATH_KEY = "dataLog_dir"
ZOOKEEPER_MYID_PATH_KEY = "myid"

ZOOKEEPER_PACKAGE_DATA_DIR_WORD = "$_dataDir_"
ZOOKEEPER_PACKAGE_DATALOG_DIR_WORD = "$_dataLogDir_"
ZOOKEEPER_PACKAGE_MYID_SRC_WORD = "$_myidSrc_"

def setupAnsibleZookeeper(rootPath, zookeepers):
    if zookeepers == None:
        print "The zookeepers map is null. Just return"
        return
    
    zookeeper_ansible_map = {}
    zookeeper_package_path = rootPath + zookeepers[serviceManagerSetupConstants.PACKAGE_KEY]
    zookeeper_template_file = rootPath + zookeepers[serviceManagerSetupConstants.TEMPLATE_KEY]
    zookeeper_install_path = zookeepers[serviceManagerSetupConstants.INSTALL_PATH_KEY]
    zookeeper_conf_path = zookeepers[serviceManagerSetupConstants.CONF_PATH_KEY]
    zookeeper_data_path = zookeepers[ZOOKEEPER_DATA_PATH_KEY]
    zookeeper_dataLog_path = zookeepers[ZOOKEEPER_DATALOG_PATH_KEY]
    zookeeper_serverScript_path = zookeepers[serviceManagerSetupConstants.SERVER_SCRPIT_PATH_KEY]
    
    devices = zookeepers[serviceManagerSetupConstants.DEVICE_KEY]
    if devices == None:
        print "The zookeeper devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The zookeeper " + deviceKey + " should not be Null"
            continue
        
        zookeeper_ansible_info = {}
        zookeeper_ansible_info[serviceManagerSetupConstants.HOST_NAME_WORD] = device[serviceManagerSetupConstants.NAME_KEY]
        zookeeper_ansible_info[serviceManagerSetupConstants.HOST_USER_WORD] = device[serviceManagerSetupConstants.USER_KEY]
        zookeeper_ansible_info[serviceManagerSetupConstants.PACKAGE_SRC_WORD] = zookeeper_package_path
        zookeeper_ansible_info[serviceManagerSetupConstants.PACKAGE_INSTALL_PATH_WORD] = zookeeper_install_path
        zookeeper_ansible_info[serviceManagerSetupConstants.CONF_SRC_WORD] = rootPath + device[serviceManagerSetupConstants.CONF_SRC_KEY]
        zookeeper_ansible_info[serviceManagerSetupConstants.CONF_TARGET_WORD] = zookeeper_conf_path
        zookeeper_ansible_info[ZOOKEEPER_PACKAGE_DATA_DIR_WORD] = zookeeper_data_path
        zookeeper_ansible_info[ZOOKEEPER_PACKAGE_DATALOG_DIR_WORD] = zookeeper_dataLog_path
        zookeeper_ansible_info[ZOOKEEPER_PACKAGE_MYID_SRC_WORD] = rootPath + device[ZOOKEEPER_MYID_PATH_KEY]
        zookeeper_ansible_info[serviceManagerSetupConstants.ANSIBLE_FILE_PATH] = rootPath + device[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        zookeeper_ansible_info[serviceManagerSetupConstants.SERVER_SCRIPT_WORD] = zookeeper_serverScript_path
        zookeeper_ansible_map[deviceKey] = zookeeper_ansible_info
        
    buildAnsibleZookeeper(zookeeper_template_file, zookeeper_ansible_map)

def buildAnsibleZookeeper(zookeeper_template_file, zookeeper_ansible_map):
    if not os.path.exists(zookeeper_template_file):
        print "zookeeper template file " + zookeeper_template_file + " is not existed"
        return -1
    
    template = open(zookeeper_template_file).read()
    
    for zookeeperAnsibleInfoKey in zookeeper_ansible_map.keys():
        zookeeperAnsibleInfo = zookeeper_ansible_map[zookeeperAnsibleInfoKey]
        if zookeeperAnsibleInfo == None:
            print "zookeeper ansible info " + zookeeperAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(serviceManagerSetupConstants.HOST_NAME_WORD, zookeeperAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.HOST_USER_WORD, zookeeperAnsibleInfo[serviceManagerSetupConstants.HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.PACKAGE_SRC_WORD, zookeeperAnsibleInfo[serviceManagerSetupConstants.PACKAGE_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.PACKAGE_INSTALL_PATH_WORD, zookeeperAnsibleInfo[serviceManagerSetupConstants.PACKAGE_INSTALL_PATH_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.CONF_SRC_WORD, zookeeperAnsibleInfo[serviceManagerSetupConstants.CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.CONF_TARGET_WORD, zookeeperAnsibleInfo[serviceManagerSetupConstants.CONF_TARGET_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_PACKAGE_DATA_DIR_WORD, zookeeperAnsibleInfo[ZOOKEEPER_PACKAGE_DATA_DIR_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_PACKAGE_DATALOG_DIR_WORD, zookeeperAnsibleInfo[ZOOKEEPER_PACKAGE_DATALOG_DIR_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_PACKAGE_MYID_SRC_WORD, zookeeperAnsibleInfo[ZOOKEEPER_PACKAGE_MYID_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.SERVER_SCRIPT_WORD, zookeeperAnsibleInfo[serviceManagerSetupConstants.SERVER_SCRIPT_WORD])
        
        zookeeperAnsibleFile = zookeeperAnsibleInfo[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        
        zookeeperAnsibleFileDir = zookeeperAnsibleFile[:zookeeperAnsibleFile.rindex("/")]
    
        if not os.path.exists(zookeeperAnsibleFileDir):
            os.makedirs(zookeeperAnsibleFileDir)
        
        if os.path.exists(zookeeperAnsibleFile):
            os.remove(zookeeperAnsibleFile)
            
        zookeeperAnsibleFileScript = os.open(zookeeperAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(zookeeperAnsibleFileScript, tempTemplate)
        os.close(zookeeperAnsibleFileScript)