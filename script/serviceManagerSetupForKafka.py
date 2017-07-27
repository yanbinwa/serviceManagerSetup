import os

DEVICE_KEY = "devices"

KAFKA_PACKAGE_KEY = "package"
KAFKA_TEMPLATE_KEY = "template"
KAFKA_INSTALL_PATH_KEY = "setup_dir"
KAFKA_CONF_PATH_KEY = "conf_dir"
KAFKA_CONF_FILE_KEY = "conf_file"
KAFKA_LOG_PATH_KEY = "log_dir"
KAFKA_SERVER_SCRPIT_PATH_KEY = "serverScript"

KAFKA_NAME_KEY = "name"
KAFKA_USER_KEY = "user"
KAFKA_CONF_SRC_KEY = "conf"
KAFKA_ANSIBLE_FILE_PATH = "ansibleFile"

KAFKA_HOST_NAME_WORD = "$_hostname_"
KAFKA_HOST_USER_WORD = "$_user_"
KAFKA_PACKAGE_SRC_WORD = "$_kafkaPackage_"
KAFKA_PACKAGE_INSTALL_WORD = "$_kafkaPackageInstallPath_"
KAFKA_CONFIG_SRC_WORD = "$_kafkaConfSrc_"
KAFKA_CONFIG_TARGET_WORD = "$_kafkaConfTarget_"
KAFKA_CONFIG_TARGET_FILE_WORD = "$_kafkaConfFile_"
KAFKA_LOG_DIR_WORD = "$_kafkaLogDir_"
KAFKA_SERVER_SCRPIT_WORD = "$_kafkaServerScript_"

def setupAnsibleKafka(rootPath, kafkas):
    if kafkas == None:
        print "The kafkas map is null. Just return"
        return
    
    kafka_ansible_map = {}
    kafka_package_path = rootPath + kafkas[KAFKA_PACKAGE_KEY]
    kafka_template_file = rootPath + kafkas[KAFKA_TEMPLATE_KEY]
    kafka_install_path = kafkas[KAFKA_INSTALL_PATH_KEY]
    kafka_conf_path = kafkas[KAFKA_CONF_PATH_KEY]
    kafka_conf_file = kafkas[KAFKA_CONF_FILE_KEY]
    kafka_log_path = kafkas[KAFKA_LOG_PATH_KEY]
    kafka_serverScript_path = kafkas[KAFKA_SERVER_SCRPIT_PATH_KEY]
    
    devices = kafkas[DEVICE_KEY]
    if devices == None:
        print "The kafka devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The kafka " + deviceKey + " should not be Null"
            continue
        
        kafka_ansible_info = {}
        kafka_ansible_info[KAFKA_HOST_NAME_WORD] = device[KAFKA_NAME_KEY]
        kafka_ansible_info[KAFKA_HOST_USER_WORD] = device[KAFKA_USER_KEY]
        kafka_ansible_info[KAFKA_PACKAGE_SRC_WORD] = kafka_package_path
        kafka_ansible_info[KAFKA_PACKAGE_INSTALL_WORD] = kafka_install_path
        kafka_ansible_info[KAFKA_CONFIG_SRC_WORD] = rootPath + device[KAFKA_CONF_SRC_KEY]
        kafka_ansible_info[KAFKA_CONFIG_TARGET_WORD] = kafka_conf_path
        kafka_ansible_info[KAFKA_CONFIG_TARGET_FILE_WORD] = kafka_conf_file
        kafka_ansible_info[KAFKA_LOG_DIR_WORD] = kafka_log_path
        kafka_ansible_info[KAFKA_ANSIBLE_FILE_PATH] = rootPath + device[KAFKA_ANSIBLE_FILE_PATH]
        kafka_ansible_info[KAFKA_SERVER_SCRPIT_WORD] = kafka_serverScript_path
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
        
        tempTemplate = template.replace(KAFKA_HOST_NAME_WORD, kafkaAnsibleInfo[KAFKA_HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(KAFKA_HOST_USER_WORD, kafkaAnsibleInfo[KAFKA_HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(KAFKA_PACKAGE_SRC_WORD, kafkaAnsibleInfo[KAFKA_PACKAGE_SRC_WORD])
        tempTemplate = tempTemplate.replace(KAFKA_PACKAGE_INSTALL_WORD, kafkaAnsibleInfo[KAFKA_PACKAGE_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(KAFKA_CONFIG_SRC_WORD, kafkaAnsibleInfo[KAFKA_CONFIG_SRC_WORD])
        tempTemplate = tempTemplate.replace(KAFKA_CONFIG_TARGET_WORD, kafkaAnsibleInfo[KAFKA_CONFIG_TARGET_WORD])
        tempTemplate = tempTemplate.replace(KAFKA_CONFIG_TARGET_FILE_WORD, kafkaAnsibleInfo[KAFKA_CONFIG_TARGET_FILE_WORD])
        tempTemplate = tempTemplate.replace(KAFKA_LOG_DIR_WORD, kafkaAnsibleInfo[KAFKA_LOG_DIR_WORD])
        tempTemplate = tempTemplate.replace(KAFKA_SERVER_SCRPIT_WORD, kafkaAnsibleInfo[KAFKA_SERVER_SCRPIT_WORD])
        
        kafkaAnsibleFile = kafkaAnsibleInfo[KAFKA_ANSIBLE_FILE_PATH]
        kafkaAnsibleFileDir = kafkaAnsibleFile[:kafkaAnsibleFile.rindex("/")]
    
        if not os.path.exists(kafkaAnsibleFileDir):
            os.makedirs(kafkaAnsibleFileDir)
        
        if os.path.exists(kafkaAnsibleFile):
            os.remove(kafkaAnsibleFile)
            
        kafkaAnsibleFileScript = os.open(kafkaAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(kafkaAnsibleFileScript, tempTemplate)
        os.close(kafkaAnsibleFileScript)