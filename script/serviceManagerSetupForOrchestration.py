import os
import serviceManagerSetupLogAgentConf
import serviceManagerSetupConstants

def setupAnsibleOrchestration(rootPath, orchestrations):
    if orchestrations == None:
        print "The orchestrations is null. Just return"
        return
    
    feature_info_map = orchestrations[serviceManagerSetupConstants.FEATURES_KEY]
    if feature_info_map == None:
        print "The orchestrations need feature map"
        return
    
    flume_info_map = feature_info_map[serviceManagerSetupConstants.FEATURES_FLUME_KEY]
    if flume_info_map == None:
        print "The flume info map should not be Null"
        return -1
    
    orchestration_ansible_map = {}
    orchestration_package_path = rootPath + orchestrations[serviceManagerSetupConstants.PACKAGE_KEY]
    orchestration_template_file = rootPath + orchestrations[serviceManagerSetupConstants.TEMPLATE_KEY]
    orchestration_install_path = orchestrations[serviceManagerSetupConstants.INSTALL_PATH_KEY]
    orchestration_log_dir = orchestrations[serviceManagerSetupConstants.LOG_PATH_KEY]
    orchestration_flume_conf_root_path = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_TARGET_ROOT_PATH_KEY]
    orchestration_flume_conf_install_path = flume_info_map[serviceManagerSetupConstants.FLUME_CONF_INSTALL_PATH_KEY]
    orchestration_flume_conf_file_name = flume_info_map[serviceManagerSetupConstants.FLUME_CONF_FILE_NAME_KEY]
    
    devices = orchestrations[serviceManagerSetupConstants.DEVICE_KEY]
    if devices == None:
        print "The orchestration devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The orchestration " + deviceKey + " should not be Null"
            continue
        
        orchestration_ansible_info = {}
        orchestration_ansible_info[serviceManagerSetupConstants.HOST_NAME_WORD] = device[serviceManagerSetupConstants.NAME_KEY]
        orchestration_ansible_info[serviceManagerSetupConstants.HOST_USER_WORD] = device[serviceManagerSetupConstants.USER_KEY]
        orchestration_ansible_info[serviceManagerSetupConstants.START_COMMAND_WORD] = device[serviceManagerSetupConstants.START_COMMAND_KEY]
        orchestration_ansible_info[serviceManagerSetupConstants.JAR_SRC_WORD] = orchestration_package_path
        orchestration_ansible_info[serviceManagerSetupConstants.JAR_INSTALL_WORD] = orchestration_install_path
        orchestration_ansible_info[serviceManagerSetupConstants.LOG_DIR_WORD] = orchestration_log_dir
        orchestration_ansible_info[serviceManagerSetupConstants.ANSIBLE_FILE_PATH] = rootPath + device[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        orchestration_ansible_info[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD] = orchestration_flume_conf_root_path + '/' + device[serviceManagerSetupConstants.NAME_KEY] + '/' + orchestration_flume_conf_file_name
        orchestration_ansible_info[serviceManagerSetupConstants.FLUME_CONF_DES_WORD] = orchestration_flume_conf_install_path
        orchestration_ansible_map[deviceKey] = orchestration_ansible_info
        
    buildAnsibleOrchestration(orchestration_template_file, orchestration_ansible_map)
    
    # Add the log file string list to flume_info_map
    flume_info_map[serviceManagerSetupConstants.LOG_FILES_KEY] = orchestrations[serviceManagerSetupConstants.LOG_FILES_KEY]
    buildFlumeConf(rootPath, flume_info_map, orchestration_ansible_map)
        
def buildAnsibleOrchestration(orchestration_template_file, orchestration_ansible_map):
    if not os.path.exists(orchestration_template_file):
        print "orchestration template file " + orchestration_template_file + " is not existed"
        return -1
    
    template = open(orchestration_template_file).read()
    for orchestrationAnsibleInfoKey in orchestration_ansible_map.keys():
        orchestrationAnsibleInfo = orchestration_ansible_map[orchestrationAnsibleInfoKey]
        if orchestrationAnsibleInfo == None:
            print "orchestration ansible info " + orchestrationAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(serviceManagerSetupConstants.HOST_NAME_WORD, orchestrationAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.HOST_USER_WORD, orchestrationAnsibleInfo[serviceManagerSetupConstants.HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_SRC_WORD, orchestrationAnsibleInfo[serviceManagerSetupConstants.JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_INSTALL_WORD, orchestrationAnsibleInfo[serviceManagerSetupConstants.JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.START_COMMAND_WORD, orchestrationAnsibleInfo[serviceManagerSetupConstants.START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.FLUME_CONF_SRC_WORD, orchestrationAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.FLUME_CONF_DES_WORD, orchestrationAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_DES_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.LOG_DIR_WORD, orchestrationAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD])
        
        orchestrationAnsibleFile = orchestrationAnsibleInfo[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        orchestrationAnsibleFileDir = orchestrationAnsibleFile[:orchestrationAnsibleFile.rindex("/")]
    
        if not os.path.exists(orchestrationAnsibleFileDir):
            os.makedirs(orchestrationAnsibleFileDir)
        
        if os.path.exists(orchestrationAnsibleFile):
            os.remove(orchestrationAnsibleFile)
            
        orchestrationAnsibleFileScript = os.open(orchestrationAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(orchestrationAnsibleFileScript, tempTemplate)
        os.close(orchestrationAnsibleFileScript)
        
def buildFlumeConf(rootPath, flume_info_map, orchestration_ansible_map):
    
    for orchestrationAnsibleInfoKey in orchestration_ansible_map.keys():
        orchestrationAnsibleInfo = orchestration_ansible_map[orchestrationAnsibleInfoKey]
        if orchestrationAnsibleInfo == None:
            print "orchestration ansible info " + orchestrationAnsibleInfo + " should not be Null"
            continue
        
        flume_conf_info = {}
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_BROKER_LIST_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_BROKER_LIST_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_LOGGING_TOPIC_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_LOGGING_TOPIC_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_PARTITION_ID_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_PARTITION_ID_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_GROUP_NAME_WORD] = 'orchestration'
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_LIST_STRING_KEY] = flume_info_map[serviceManagerSetupConstants.LOG_FILES_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TEMPLATE_KEY] = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_TEMPLATE_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_SRC_TEMPLATE_KEY] = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_SRC_TEMPLATE_KEY]
        
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_PATH_WORD] = orchestrationAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_NAME_WORD] = orchestrationAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TARGET_PATH_KEY] = orchestrationAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD]
        
        serviceManagerSetupLogAgentConf.buildFlumeLogAgentConf(flume_conf_info)