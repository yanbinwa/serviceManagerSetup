import os

DEVICE_KEY = "devices"

ZOOKEEPER_PACKAGE_KEY = "package"
ZOOKEEPER_TEMPLATE_KEY = "template"
ZOOKEEPER_INSTALL_PATH_KEY = "setup_dir"
ZOOKEEPER_CONF_PATH_KEY = "conf_dir"
ZOOKEEPER_DATA_PATH_KEY = "data_dir"
ZOOKEEPER_DATALOG_PATH_KEY = "dataLog_dir"
ZOOKEEPER_SERVER_SCRPIT_PATH_KEY = "serverScript"

ZOOKEEPER_NAME_KEY = "name"
ZOOKEEPER_USER_KEY = "user"
ZOOKEEPER_MYID_PATH_KEY = "myid"
ZOOKEEPER_CONF_SRC_KEY = "conf"
ZOOKEEPER_ANSIBLE_FILE_PATH = "ansibleFile"

ZOOKEEPER_HOST_NAME_WORD = "$_hostname_"
ZOOKEEPER_HOST_USER_WORD = "$_user_"
ZOOKEEPER_PACKAGE_SRC_WORD = "$_zookeeperPackage_"
ZOOKEEPER_PACKAGE_INSTALL_WORD = "$_zookeeperPackageInstallPath_"
ZOOKEEPER_CONFIG_SRC_WORD = "$_zookeeperConfSrc_"
ZOOKEEPER_CONFIG_TARGET_WORD = "$_zookeeperConfTarget_"
ZOOKEEPER_DATA_DIR_WORD = "$_zookeeperDataDir_"
ZOOKEEPER_DATALOG_DIR_WORD = "$_zookeeperDataLogDir_"
ZOOKEEPER_MYID_SRC_WORD = "$_zookeeperMyidSrc_"
ZOOKEEPER_SERVER_SCRPIT_WORD = "$_zookeeperServerScript_"

def setupAnsibleZookeeper(rootPath, zookeepers):
    if zookeepers == None:
        print "The zookeepers map should not be Null"
        return -1
    
    zookeeper_ansible_map = {}
    zookeeper_package_path = rootPath + zookeepers[ZOOKEEPER_PACKAGE_KEY]
    zookeeper_template_file = rootPath + zookeepers[ZOOKEEPER_TEMPLATE_KEY]
    zookeeper_install_path = zookeepers[ZOOKEEPER_INSTALL_PATH_KEY]
    zookeeper_conf_path = zookeepers[ZOOKEEPER_CONF_PATH_KEY]
    zookeeper_data_path = zookeepers[ZOOKEEPER_DATA_PATH_KEY]
    zookeeper_dataLog_path = zookeepers[ZOOKEEPER_DATALOG_PATH_KEY]
    zookeeper_serverScript_path = zookeepers[ZOOKEEPER_SERVER_SCRPIT_PATH_KEY]
    
    devices = zookeepers[DEVICE_KEY]
    if devices == None:
        print "The zookeeper devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The zookeeper " + deviceKey + " should not be Null"
            continue
        
        zookeeper_ansible_info = {}
        zookeeper_ansible_info[ZOOKEEPER_HOST_NAME_WORD] = device[ZOOKEEPER_NAME_KEY]
        zookeeper_ansible_info[ZOOKEEPER_HOST_USER_WORD] = device[ZOOKEEPER_USER_KEY]
        zookeeper_ansible_info[ZOOKEEPER_PACKAGE_SRC_WORD] = zookeeper_package_path
        zookeeper_ansible_info[ZOOKEEPER_PACKAGE_INSTALL_WORD] = zookeeper_install_path
        zookeeper_ansible_info[ZOOKEEPER_CONFIG_SRC_WORD] = rootPath + device[ZOOKEEPER_CONF_SRC_KEY]
        zookeeper_ansible_info[ZOOKEEPER_CONFIG_TARGET_WORD] = zookeeper_conf_path
        zookeeper_ansible_info[ZOOKEEPER_DATA_DIR_WORD] = zookeeper_data_path
        zookeeper_ansible_info[ZOOKEEPER_DATALOG_DIR_WORD] = zookeeper_dataLog_path
        zookeeper_ansible_info[ZOOKEEPER_MYID_SRC_WORD] = rootPath + device[ZOOKEEPER_MYID_PATH_KEY]
        zookeeper_ansible_info[ZOOKEEPER_ANSIBLE_FILE_PATH] = rootPath + device[ZOOKEEPER_ANSIBLE_FILE_PATH]
        zookeeper_ansible_info[ZOOKEEPER_SERVER_SCRPIT_WORD] = zookeeper_serverScript_path
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
        
        tempTemplate = template.replace(ZOOKEEPER_HOST_NAME_WORD, zookeeperAnsibleInfo[ZOOKEEPER_HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_HOST_USER_WORD, zookeeperAnsibleInfo[ZOOKEEPER_HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_PACKAGE_SRC_WORD, zookeeperAnsibleInfo[ZOOKEEPER_PACKAGE_SRC_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_PACKAGE_INSTALL_WORD, zookeeperAnsibleInfo[ZOOKEEPER_PACKAGE_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_CONFIG_SRC_WORD, zookeeperAnsibleInfo[ZOOKEEPER_CONFIG_SRC_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_CONFIG_TARGET_WORD, zookeeperAnsibleInfo[ZOOKEEPER_CONFIG_TARGET_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_DATA_DIR_WORD, zookeeperAnsibleInfo[ZOOKEEPER_DATA_DIR_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_DATALOG_DIR_WORD, zookeeperAnsibleInfo[ZOOKEEPER_DATALOG_DIR_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_MYID_SRC_WORD, zookeeperAnsibleInfo[ZOOKEEPER_MYID_SRC_WORD])
        tempTemplate = tempTemplate.replace(ZOOKEEPER_SERVER_SCRPIT_WORD, zookeeperAnsibleInfo[ZOOKEEPER_SERVER_SCRPIT_WORD])
        
        zookeeperAnsibleFile = zookeeperAnsibleInfo[ZOOKEEPER_ANSIBLE_FILE_PATH]
        if os.path.exists(zookeeperAnsibleFile):
            os.remove(zookeeperAnsibleFile)
            
        zookeeperAnsibleFileScript = os.open(zookeeperAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(zookeeperAnsibleFileScript, tempTemplate)