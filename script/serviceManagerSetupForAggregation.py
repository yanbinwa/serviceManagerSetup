import os
import serviceManagerSetupLogAgentConf

DEVICE_KEY = "devices"

AGGREGATION_PACKAGE_KEY = "package"
AGGREGATION_TEMPLATE_KEY = "template"
AGGREGATION_INSTALL_PATH_KEY = "setup_dir"
AGGREGATION_LOG_PATH_KEY = "logFilePath"
AGGREGATION_LOG_FILES_KEY = "logFiles"
AGGREGATION_FLUME_INFO_KEY = "flume"

AGGREGATION_NAME_KEY = "name"
AGGREGATION_USER_KEY = "user"
AGGREGATION_START_COMMAND_KEY = "command"

AGGREGATION_ANSIBLE_FILE_PATH = "ansibleFile" 

AGGREGATION_HOST_NAME_WORD = "$_hostname_"
AGGREGATION_HOST_USER_WORD = "$_user_"
AGGREGATION_JAR_SRC_WORD = "$_aggregationJarSrc_"
AGGREGATION_JAR_INSTALL_WORD = "$_aggregationJarInstallPath_"
AGGREGATION_LOG_DIR_WORD = "$_aggregationLogDir_"
AGGREGATION_START_COMMAND_WORD = "$_aggregationStartCommand_"
AGGREGATION_FLUME_CONF_SRC_WORD = "$_aggregationFlumeConfSrc_"
AGGREGATION_FLUME_CONF_DES_WORD = "$_flumeConfPath_"

FLUME_CONF_TARGET_ROOT_PATH_KEY = "flumeConfTargetRootPath"
FLUME_CONF_INSTALL_PATH_KEY = "flumeConfInstallPath"
FLUME_CONF_FILE_NAME_KEY = "flumeConfName"
FLUME_CONF_TEMPLATE_KEY = "flumeConfTemplate"
FLUME_CONF_SRC_TEMPLATE_KEY = "flumeConfSrcTemplate"
FLUME_KAFKA_BROKER_LIST_KEY = "kafkaBrokerList"
FLUME_KAFKA_LOGGING_TOPIC_KEY = "kafkaTopic"
FLUME_KAFKA_PARTITION_ID_KEY = "kafkaPartitionId"

def setupAnsibleAggregation(rootPath, aggregations):
    if aggregations == None:
        print "The aggregations map should not be Null"
        return -1
    
    flume_info_map = aggregations[AGGREGATION_FLUME_INFO_KEY]
    if flume_info_map == None:
        print "The flume info map should not be Null"
        return -1
    
    aggregation_ansible_map = {}
    aggregation_package_path = rootPath + aggregations[AGGREGATION_PACKAGE_KEY]
    aggregation_template_file = rootPath + aggregations[AGGREGATION_TEMPLATE_KEY]
    aggregation_install_path = aggregations[AGGREGATION_INSTALL_PATH_KEY]
    aggregation_log_path = aggregations[AGGREGATION_LOG_PATH_KEY]
    aggregation_flume_conf_root_path = rootPath + flume_info_map[FLUME_CONF_TARGET_ROOT_PATH_KEY]
    aggregation_flume_conf_install_path = flume_info_map[FLUME_CONF_INSTALL_PATH_KEY]
    aggregation_flume_conf_file_name = flume_info_map[FLUME_CONF_FILE_NAME_KEY]
    
    devices = aggregations[DEVICE_KEY]
    
    if devices == None:
        print "The aggregation devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The aggregation " + deviceKey + " should not be Null"
            continue
        
        aggregation_ansible_info = {}
        aggregation_ansible_info[AGGREGATION_HOST_NAME_WORD] = device[AGGREGATION_NAME_KEY]
        aggregation_ansible_info[AGGREGATION_HOST_USER_WORD] = device[AGGREGATION_USER_KEY]
        aggregation_ansible_info[AGGREGATION_START_COMMAND_WORD] = device[AGGREGATION_START_COMMAND_KEY]
        aggregation_ansible_info[AGGREGATION_JAR_SRC_WORD] = aggregation_package_path
        aggregation_ansible_info[AGGREGATION_JAR_INSTALL_WORD] = aggregation_install_path
        aggregation_ansible_info[AGGREGATION_LOG_DIR_WORD] = aggregation_log_path
        aggregation_ansible_info[AGGREGATION_ANSIBLE_FILE_PATH] = rootPath + device[AGGREGATION_ANSIBLE_FILE_PATH]
        aggregation_ansible_info[AGGREGATION_FLUME_CONF_SRC_WORD] = aggregation_flume_conf_root_path + '/' + device[AGGREGATION_NAME_KEY] + '/' + aggregation_flume_conf_file_name
        aggregation_ansible_info[AGGREGATION_FLUME_CONF_DES_WORD] = aggregation_flume_conf_install_path
        
        aggregation_ansible_map[deviceKey] = aggregation_ansible_info
    
    buildAnsibleAggregation(aggregation_template_file, aggregation_ansible_map)
    
    flume_info_map[AGGREGATION_LOG_FILES_KEY] = aggregations[AGGREGATION_LOG_FILES_KEY]
    buildFlumeConf(rootPath, flume_info_map, aggregation_ansible_map)
        
def buildAnsibleAggregation(aggregation_template_file, aggregation_ansible_map):
    if not os.path.exists(aggregation_template_file):
        print "aggregation template file " + aggregation_template_file + " is not existed"
        return -1
    
    template = open(aggregation_template_file).read()
    for aggregationAnsibleInfoKey in aggregation_ansible_map.keys():
        aggregationAnsibleInfo = aggregation_ansible_map[aggregationAnsibleInfoKey]
        if aggregationAnsibleInfo == None:
            print "aggregation ansible info " + aggregationAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(AGGREGATION_HOST_NAME_WORD, aggregationAnsibleInfo[AGGREGATION_HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(AGGREGATION_HOST_USER_WORD, aggregationAnsibleInfo[AGGREGATION_HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(AGGREGATION_JAR_SRC_WORD, aggregationAnsibleInfo[AGGREGATION_JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(AGGREGATION_JAR_INSTALL_WORD, aggregationAnsibleInfo[AGGREGATION_JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(AGGREGATION_START_COMMAND_WORD, aggregationAnsibleInfo[AGGREGATION_START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(AGGREGATION_FLUME_CONF_SRC_WORD, aggregationAnsibleInfo[AGGREGATION_FLUME_CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(AGGREGATION_FLUME_CONF_DES_WORD, aggregationAnsibleInfo[AGGREGATION_FLUME_CONF_DES_WORD])
        tempTemplate = tempTemplate.replace(AGGREGATION_LOG_DIR_WORD, aggregationAnsibleInfo[AGGREGATION_LOG_DIR_WORD])
        
        aggregationAnsibleFile = aggregationAnsibleInfo[AGGREGATION_ANSIBLE_FILE_PATH]
        aggregationAnsibleFileDir = aggregationAnsibleFile[:aggregationAnsibleFile.rindex("/")]
    
        if not os.path.exists(aggregationAnsibleFileDir):
            os.makedirs(aggregationAnsibleFileDir)
        
        if os.path.exists(aggregationAnsibleFile):
            os.remove(aggregationAnsibleFile)
            
        aggregationAnsibleFileScript = os.open(aggregationAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(aggregationAnsibleFileScript, tempTemplate)
        os.close(aggregationAnsibleFileScript)

def buildFlumeConf(rootPath, flume_info_map, aggregation_ansible_map):
    
    for aggregationAnsibleInfoKey in aggregation_ansible_map.keys():
        aggregationAnsibleInfo = aggregation_ansible_map[aggregationAnsibleInfoKey]
        if aggregationAnsibleInfo == None:
            print "aggregation ansible info " + aggregationAnsibleInfo + " should not be Null"
            continue
        
        flume_conf_info = {}
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_BROKER_LIST_WORD] = flume_info_map[FLUME_KAFKA_BROKER_LIST_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_LOGGING_TOPIC_WORD] = flume_info_map[FLUME_KAFKA_LOGGING_TOPIC_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_PARTITION_ID_WORD] = flume_info_map[FLUME_KAFKA_PARTITION_ID_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_GROUP_NAME_WORD] = 'aggregation'
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_LIST_STRING_KEY] = flume_info_map[AGGREGATION_LOG_FILES_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TEMPLATE_KEY] = rootPath + flume_info_map[FLUME_CONF_TEMPLATE_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_SRC_TEMPLATE_KEY] = rootPath + flume_info_map[FLUME_CONF_SRC_TEMPLATE_KEY]
        
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_NAME_WORD] = aggregationAnsibleInfo[AGGREGATION_HOST_NAME_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_PATH_WORD] = aggregationAnsibleInfo[AGGREGATION_LOG_DIR_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TARGET_PATH_KEY] = aggregationAnsibleInfo[AGGREGATION_FLUME_CONF_SRC_WORD]
        
        serviceManagerSetupLogAgentConf.buildFlumeLogAgentConf(flume_conf_info)