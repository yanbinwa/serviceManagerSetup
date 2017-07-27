import os
import serviceManagerSetupLogAgentConf

DEVICE_KEY = "devices"

ORCHESTRATION_PACKAGE_KEY = "package"
ORCHESTRATION_TEMPLATE_KEY = "template"
ORCHESTRATION_INSTALL_PATH_KEY = "setup_dir"
ORCHESTRATION_LOG_PATH_KEY = "logFilePath"
ORCHESTRATION_LOG_FILES_KEY = "logFiles"
ORCHESTRATION_FLUME_INFO_KEY = "flume"

ORCHESTRATION_NAME_KEY = "name"
ORCHESTRATION_USER_KEY = "user"
ORCHESTRATION_START_COMMAND_KEY = "command"

ORCHESTRATION_ANSIBLE_FILE_PATH = "ansibleFile" 

ORCHESTRATION_HOST_NAME_WORD = "$_hostname_"
ORCHESTRATION_HOST_USER_WORD = "$_user_"
ORCHESTRATION_JAR_SRC_WORD = "$_orchestrationJarSrc_"
ORCHESTRATION_JAR_INSTALL_WORD = "$_orchestrationJarInstallPath_"
ORCHESTRATION_LOG_DIR_WORD = "$_orchestrationLogDir_"
ORCHESTRATION_START_COMMAND_WORD = "$_orchestrationStartCommand_"
ORCHESTRATION_FLUME_CONF_SRC_WORD = "$_orchestrationFlumeConfSrc_"
ORCHESTRATION_FLUME_CONF_DES_WORD = "$_flumeConfPath_"

FLUME_CONF_TARGET_ROOT_PATH_KEY = "flumeConfTargetRootPath"
FLUME_CONF_INSTALL_PATH_KEY = "flumeConfInstallPath"
FLUME_CONF_FILE_NAME_KEY = "flumeConfName"
FLUME_CONF_TEMPLATE_KEY = "flumeConfTemplate"
FLUME_CONF_SRC_TEMPLATE_KEY = "flumeConfSrcTemplate"
FLUME_KAFKA_BROKER_LIST_KEY = "kafkaBrokerList"
FLUME_KAFKA_LOGGING_TOPIC_KEY = "kafkaTopic"
FLUME_KAFKA_PARTITION_ID_KEY = "kafkaPartitionId"

def setupAnsibleOrchestration(rootPath, orchestrations):
    if orchestrations == None:
        print "The orchestrations is null. Just return"
        return
    
    flume_info_map = orchestrations[ORCHESTRATION_FLUME_INFO_KEY]
    if flume_info_map == None:
        print "The flume info map should not be Null"
        return -1
    
    orchestration_ansible_map = {}
    orchestration_package_path = rootPath + orchestrations[ORCHESTRATION_PACKAGE_KEY]
    orchestration_template_file = rootPath + orchestrations[ORCHESTRATION_TEMPLATE_KEY]
    orchestration_install_path = orchestrations[ORCHESTRATION_INSTALL_PATH_KEY]
    orchestration_log_dir = orchestrations[ORCHESTRATION_LOG_PATH_KEY]
    orchestration_flume_conf_root_path = rootPath + flume_info_map[FLUME_CONF_TARGET_ROOT_PATH_KEY]
    orchestration_flume_conf_install_path = flume_info_map[FLUME_CONF_INSTALL_PATH_KEY]
    orchestration_flume_conf_file_name = flume_info_map[FLUME_CONF_FILE_NAME_KEY]
    
    devices = orchestrations[DEVICE_KEY]
    if devices == None:
        print "The orchestration devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The orchestration " + deviceKey + " should not be Null"
            continue
        
        orchestration_ansible_info = {}
        orchestration_ansible_info[ORCHESTRATION_HOST_NAME_WORD] = device[ORCHESTRATION_NAME_KEY]
        orchestration_ansible_info[ORCHESTRATION_HOST_USER_WORD] = device[ORCHESTRATION_USER_KEY]
        orchestration_ansible_info[ORCHESTRATION_START_COMMAND_WORD] = device[ORCHESTRATION_START_COMMAND_KEY]
        orchestration_ansible_info[ORCHESTRATION_JAR_SRC_WORD] = orchestration_package_path
        orchestration_ansible_info[ORCHESTRATION_JAR_INSTALL_WORD] = orchestration_install_path
        orchestration_ansible_info[ORCHESTRATION_LOG_DIR_WORD] = orchestration_log_dir
        orchestration_ansible_info[ORCHESTRATION_ANSIBLE_FILE_PATH] = rootPath + device[ORCHESTRATION_ANSIBLE_FILE_PATH]
        orchestration_ansible_info[ORCHESTRATION_FLUME_CONF_SRC_WORD] = orchestration_flume_conf_root_path + '/' + device[ORCHESTRATION_NAME_KEY] + '/' + orchestration_flume_conf_file_name
        orchestration_ansible_info[ORCHESTRATION_FLUME_CONF_DES_WORD] = orchestration_flume_conf_install_path
        orchestration_ansible_map[deviceKey] = orchestration_ansible_info
        
    buildAnsibleOrchestration(orchestration_template_file, orchestration_ansible_map)
    
    # Add the log file string list to flume_info_map
    flume_info_map[ORCHESTRATION_LOG_FILES_KEY] = orchestrations[ORCHESTRATION_LOG_FILES_KEY]
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
        
        tempTemplate = template.replace(ORCHESTRATION_HOST_NAME_WORD, orchestrationAnsibleInfo[ORCHESTRATION_HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_HOST_USER_WORD, orchestrationAnsibleInfo[ORCHESTRATION_HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_JAR_SRC_WORD, orchestrationAnsibleInfo[ORCHESTRATION_JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_JAR_INSTALL_WORD, orchestrationAnsibleInfo[ORCHESTRATION_JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_START_COMMAND_WORD, orchestrationAnsibleInfo[ORCHESTRATION_START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_FLUME_CONF_SRC_WORD, orchestrationAnsibleInfo[ORCHESTRATION_FLUME_CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_FLUME_CONF_DES_WORD, orchestrationAnsibleInfo[ORCHESTRATION_FLUME_CONF_DES_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_LOG_DIR_WORD, orchestrationAnsibleInfo[ORCHESTRATION_LOG_DIR_WORD])
        
        orchestrationAnsibleFile = orchestrationAnsibleInfo[ORCHESTRATION_ANSIBLE_FILE_PATH]
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
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_BROKER_LIST_WORD] = flume_info_map[FLUME_KAFKA_BROKER_LIST_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_LOGGING_TOPIC_WORD] = flume_info_map[FLUME_KAFKA_LOGGING_TOPIC_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_PARTITION_ID_WORD] = flume_info_map[FLUME_KAFKA_PARTITION_ID_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_GROUP_NAME_WORD] = 'orchestration'
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_LIST_STRING_KEY] = flume_info_map[ORCHESTRATION_LOG_FILES_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TEMPLATE_KEY] = rootPath + flume_info_map[FLUME_CONF_TEMPLATE_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_SRC_TEMPLATE_KEY] = rootPath + flume_info_map[FLUME_CONF_SRC_TEMPLATE_KEY]
        
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_PATH_WORD] = orchestrationAnsibleInfo[ORCHESTRATION_LOG_DIR_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_NAME_WORD] = orchestrationAnsibleInfo[ORCHESTRATION_HOST_NAME_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TARGET_PATH_KEY] = orchestrationAnsibleInfo[ORCHESTRATION_FLUME_CONF_SRC_WORD]
        
        serviceManagerSetupLogAgentConf.buildFlumeLogAgentConf(flume_conf_info)