import os
import serviceManagerSetupConstants

#Specific 

CONFIG_MANIFEST_SRC_KEY='manifest_src'
CONFIG_MANIFEST_TARGET_KEY='manifest_target'
CONFIG_CONF_DIR_KEY='conf_dir'

CONFIG_MANIFEST_SRC_WORD='$_manifestSrc_'
CONFIG_MANIFEST_TARGET_WORD='$_manifestTarget_'
CONFIG_CONF_DIR_WORD='$_confDir_'

def setupAnsibleConfig(rootPath, configs):
    if configs == None:
        print "The configs map should not be Null"
        return -1
    
    config_ansible_map = {}
    config_package_path = rootPath + configs[serviceManagerSetupConstants.PACKAGE_KEY]
    config_template_file = rootPath + configs[serviceManagerSetupConstants.TEMPLATE_KEY]
    config_install_path = configs[serviceManagerSetupConstants.INSTALL_PATH_KEY]
    config_log_dir = configs[serviceManagerSetupConstants.LOG_PATH_KEY]
    config_manifest_src = rootPath + configs[CONFIG_MANIFEST_SRC_KEY]
    config_manifest_target = configs[CONFIG_MANIFEST_TARGET_KEY]
    config_conf_dir = configs[CONFIG_CONF_DIR_KEY]
    
    devices = configs[serviceManagerSetupConstants.DEVICE_KEY]
    if devices == None:
        print "The configs devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The config " + deviceKey + " should not be Null"
            continue
        
        config_ansible_info = {}
        config_ansible_info[serviceManagerSetupConstants.HOST_NAME_WORD] = device[serviceManagerSetupConstants.NAME_KEY]
        config_ansible_info[serviceManagerSetupConstants.HOST_USER_WORD] = device[serviceManagerSetupConstants.USER_KEY]
        config_ansible_info[serviceManagerSetupConstants.START_COMMAND_WORD] = device[serviceManagerSetupConstants.START_COMMAND_KEY]
        config_ansible_info[serviceManagerSetupConstants.JAR_SRC_WORD] = config_package_path
        config_ansible_info[serviceManagerSetupConstants.JAR_INSTALL_WORD] = config_install_path
        config_ansible_info[serviceManagerSetupConstants.LOG_DIR_WORD] = config_log_dir
        config_ansible_info[serviceManagerSetupConstants.ANSIBLE_FILE_PATH] = rootPath + device[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        
        config_ansible_info[CONFIG_MANIFEST_SRC_WORD] = config_manifest_src
        config_ansible_info[CONFIG_MANIFEST_TARGET_WORD] = config_manifest_target
        config_ansible_info[CONFIG_CONF_DIR_WORD] = config_conf_dir
        
        config_ansible_map[deviceKey] = config_ansible_info
        
    buildAnsibleConfig(config_template_file, config_ansible_map)
        
def buildAnsibleConfig(config_template_file, config_ansible_map):
    if not os.path.exists(config_template_file):
        print "config template file " + config_template_file + " is not existed"
        return -1
    
    template = open(config_template_file).read()
    for configAnsibleInfoKey in config_ansible_map.keys():
        configAnsibleInfo = config_ansible_map[configAnsibleInfoKey]
        if configAnsibleInfo == None:
            print "config ansible info " + configAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(serviceManagerSetupConstants.HOST_NAME_WORD, configAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.HOST_USER_WORD, configAnsibleInfo[serviceManagerSetupConstants.HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_SRC_WORD, configAnsibleInfo[serviceManagerSetupConstants.JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_INSTALL_WORD, configAnsibleInfo[serviceManagerSetupConstants.JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.START_COMMAND_WORD, configAnsibleInfo[serviceManagerSetupConstants.START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.LOG_DIR_WORD, configAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD])
        
        tempTemplate = tempTemplate.replace(CONFIG_MANIFEST_SRC_WORD, configAnsibleInfo[CONFIG_MANIFEST_SRC_WORD])
        tempTemplate = tempTemplate.replace(CONFIG_MANIFEST_TARGET_WORD, configAnsibleInfo[CONFIG_MANIFEST_TARGET_WORD])
        tempTemplate = tempTemplate.replace(CONFIG_CONF_DIR_WORD, configAnsibleInfo[CONFIG_CONF_DIR_WORD])
        
        configAnsibleFile = configAnsibleInfo[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        configAnsibleFileDir = configAnsibleFile[:configAnsibleFile.rindex("/")]
    
        if not os.path.exists(configAnsibleFileDir):
            os.makedirs(configAnsibleFileDir)
        
        if os.path.exists(configAnsibleFile):
            os.remove(configAnsibleFile)
            
        configAnsibleFileScript = os.open(configAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(configAnsibleFileScript, tempTemplate)
        os.close(configAnsibleFileScript)
        