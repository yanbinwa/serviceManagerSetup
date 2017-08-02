import os
import serviceManagerSetupLogAgentConf
import serviceManagerSetupConstants

def setupAnsibleAggregation(rootPath, aggregations):
    if aggregations == None:
        print "The aggregations map is Null. Just return"
        return
    
    feature_info_map = aggregations[serviceManagerSetupConstants.FEATURES_KEY]
    if feature_info_map == None:
        print "The aggregations need feature map"
        return
    
    flume_info_map = feature_info_map[serviceManagerSetupConstants.FEATURES_FLUME_KEY]
    if flume_info_map == None:
        print "The flume info map should not be Null"
        return -1
    
    aggregation_ansible_map = {}
    aggregation_package_path = rootPath + aggregations[serviceManagerSetupConstants.PACKAGE_KEY]
    aggregation_template_file = rootPath + aggregations[serviceManagerSetupConstants.TEMPLATE_KEY]
    aggregation_install_path = aggregations[serviceManagerSetupConstants.INSTALL_PATH_KEY]
    aggregation_log_path = aggregations[serviceManagerSetupConstants.LOG_PATH_KEY]
    aggregation_flume_conf_root_path = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_TARGET_ROOT_PATH_KEY]
    aggregation_flume_conf_install_path = flume_info_map[serviceManagerSetupConstants.FLUME_CONF_INSTALL_PATH_KEY]
    aggregation_flume_conf_file_name = flume_info_map[serviceManagerSetupConstants.FLUME_CONF_FILE_NAME_KEY]
    
    devices = aggregations[serviceManagerSetupConstants.DEVICE_KEY]
    
    if devices == None:
        print "The aggregation devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The aggregation " + deviceKey + " should not be Null"
            continue
        
        aggregation_ansible_info = {}
        aggregation_ansible_info[serviceManagerSetupConstants.HOST_NAME_WORD] = device[serviceManagerSetupConstants.NAME_KEY]
        aggregation_ansible_info[serviceManagerSetupConstants.HOST_USER_WORD] = device[serviceManagerSetupConstants.USER_KEY]
        aggregation_ansible_info[serviceManagerSetupConstants.START_COMMAND_WORD] = device[serviceManagerSetupConstants.START_COMMAND_KEY]
        aggregation_ansible_info[serviceManagerSetupConstants.JAR_SRC_WORD] = aggregation_package_path
        aggregation_ansible_info[serviceManagerSetupConstants.JAR_INSTALL_WORD] = aggregation_install_path
        aggregation_ansible_info[serviceManagerSetupConstants.LOG_DIR_WORD] = aggregation_log_path
        aggregation_ansible_info[serviceManagerSetupConstants.ANSIBLE_FILE_PATH] = rootPath + device[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        aggregation_ansible_info[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD] = aggregation_flume_conf_root_path + '/' + device[serviceManagerSetupConstants.NAME_KEY] + '/' + aggregation_flume_conf_file_name
        aggregation_ansible_info[serviceManagerSetupConstants.FLUME_CONF_DES_WORD] = aggregation_flume_conf_install_path
        
        aggregation_ansible_map[deviceKey] = aggregation_ansible_info
    
    buildAnsibleAggregation(aggregation_template_file, aggregation_ansible_map)
    
    flume_info_map[serviceManagerSetupConstants.LOG_FILES_KEY] = aggregations[serviceManagerSetupConstants.LOG_FILES_KEY]
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
        
        tempTemplate = template.replace(serviceManagerSetupConstants.HOST_NAME_WORD, aggregationAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.HOST_USER_WORD, aggregationAnsibleInfo[serviceManagerSetupConstants.HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_SRC_WORD, aggregationAnsibleInfo[serviceManagerSetupConstants.JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_INSTALL_WORD, aggregationAnsibleInfo[serviceManagerSetupConstants.JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.START_COMMAND_WORD, aggregationAnsibleInfo[serviceManagerSetupConstants.START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.FLUME_CONF_SRC_WORD, aggregationAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.FLUME_CONF_DES_WORD, aggregationAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_DES_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.LOG_DIR_WORD, aggregationAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD])
        
        aggregationAnsibleFile = aggregationAnsibleInfo[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
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
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_BROKER_LIST_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_BROKER_LIST_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_LOGGING_TOPIC_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_LOGGING_TOPIC_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_PARTITION_ID_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_PARTITION_ID_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_GROUP_NAME_WORD] = 'aggregation'
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_LIST_STRING_KEY] = flume_info_map[serviceManagerSetupConstants.LOG_FILES_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TEMPLATE_KEY] = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_TEMPLATE_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_SRC_TEMPLATE_KEY] = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_SRC_TEMPLATE_KEY]
        
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_NAME_WORD] = aggregationAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_PATH_WORD] = aggregationAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TARGET_PATH_KEY] = aggregationAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD]
        
        serviceManagerSetupLogAgentConf.buildFlumeLogAgentConf(flume_conf_info)