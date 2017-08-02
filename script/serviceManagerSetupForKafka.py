import os
import serviceManagerSetupConstants

KAFKA_LOG_DIR_KEY = "log_dir"

KAFKA_LOG_DIR_WORD = "$_logDir_"

def setupAnsibleKafka(rootPath, kafkas):
    if kafkas == None:
        print "The kafkas map is null. Just return"
        return
    
    kafka_ansible_map = {}
    kafka_package_path = rootPath + kafkas[serviceManagerSetupConstants.PACKAGE_KEY]
    kafka_template_file = rootPath + kafkas[serviceManagerSetupConstants.TEMPLATE_KEY]
    kafka_install_path = kafkas[serviceManagerSetupConstants.INSTALL_PATH_KEY]
    kafka_conf_path = kafkas[serviceManagerSetupConstants.CONF_PATH_KEY]
    kafka_log_path = kafkas[KAFKA_LOG_DIR_KEY]
    kafka_serverScript_path = kafkas[serviceManagerSetupConstants.SERVER_SCRPIT_PATH_KEY]
    
    devices = kafkas[serviceManagerSetupConstants.DEVICE_KEY]
    if devices == None:
        print "The kafka devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The kafka " + deviceKey + " should not be Null"
            continue
        
        kafka_ansible_info = {}
        kafka_ansible_info[serviceManagerSetupConstants.HOST_NAME_WORD] = device[serviceManagerSetupConstants.NAME_KEY]
        kafka_ansible_info[serviceManagerSetupConstants.HOST_USER_WORD] = device[serviceManagerSetupConstants.USER_KEY]
        kafka_ansible_info[serviceManagerSetupConstants.PACKAGE_SRC_WORD] = kafka_package_path
        kafka_ansible_info[serviceManagerSetupConstants.PACKAGE_INSTALL_PATH_WORD] = kafka_install_path
        kafka_ansible_info[serviceManagerSetupConstants.CONF_SRC_WORD] = rootPath + device[serviceManagerSetupConstants.CONF_SRC_KEY]
        kafka_ansible_info[serviceManagerSetupConstants.CONF_TARGET_WORD] = kafka_conf_path
        kafka_ansible_info[KAFKA_LOG_DIR_WORD] = kafka_log_path
        kafka_ansible_info[serviceManagerSetupConstants.ANSIBLE_FILE_PATH] = rootPath + device[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        kafka_ansible_info[serviceManagerSetupConstants.SERVER_SCRIPT_WORD] = kafka_serverScript_path
        kafka_ansible_map[deviceKey] = kafka_ansible_info
        
    buildAnsibleKafka(kafka_template_file, kafka_ansible_map)

def buildAnsibleKafka(kafka_template_file, kafka_ansible_map):
    if not os.path.exists(kafka_template_file):
        print "kafka template file " + kafka_template_file + " is not existed"
        return -1
    
    template = open(kafka_template_file).read()
    
    for kafkaAnsibleInfoKey in kafka_ansible_map.keys():
        kafkaAnsibleInfo = kafka_ansible_map[kafkaAnsibleInfoKey]
        if kafkaAnsibleInfo == None:
            print "kafka ansible info " + kafkaAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(serviceManagerSetupConstants.HOST_NAME_WORD, kafkaAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.HOST_USER_WORD, kafkaAnsibleInfo[serviceManagerSetupConstants.HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.PACKAGE_SRC_WORD, kafkaAnsibleInfo[serviceManagerSetupConstants.PACKAGE_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.PACKAGE_INSTALL_PATH_WORD, kafkaAnsibleInfo[serviceManagerSetupConstants.PACKAGE_INSTALL_PATH_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.CONF_SRC_WORD, kafkaAnsibleInfo[serviceManagerSetupConstants.CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.CONF_TARGET_WORD, kafkaAnsibleInfo[serviceManagerSetupConstants.CONF_TARGET_WORD])
        tempTemplate = tempTemplate.replace(KAFKA_LOG_DIR_WORD, kafkaAnsibleInfo[KAFKA_LOG_DIR_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.SERVER_SCRIPT_WORD, kafkaAnsibleInfo[serviceManagerSetupConstants.SERVER_SCRIPT_WORD])
        
        kafkaAnsibleFile = kafkaAnsibleInfo[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        kafkaAnsibleFileDir = kafkaAnsibleFile[:kafkaAnsibleFile.rindex("/")]
    
        if not os.path.exists(kafkaAnsibleFileDir):
            os.makedirs(kafkaAnsibleFileDir)
        
        if os.path.exists(kafkaAnsibleFile):
            os.remove(kafkaAnsibleFile)
            
        kafkaAnsibleFileScript = os.open(kafkaAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(kafkaAnsibleFileScript, tempTemplate)
        os.close(kafkaAnsibleFileScript)