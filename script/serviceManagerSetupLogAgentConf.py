import os

KAFKA_BROKER_LIST_WORD = "$_kafkaBrokerList_"
KAFKA_LOGGING_TOPIC_WORD = "$_kafkaTopic_"
SERVICE_GROUP_NAME_WORD = "$_serviceGroupName_"
SERVICE_NAME_WORD = "$_serviceName_"
LOG_FILE_PATH_WORD = "$_logFilePath_"
FLUME_CONF_TARGET_PATH_KEY = "flumeConfTargetPath"

def buildFlumeLogAgentConf(flume_Conf_Template_file, flumeLogAgentProperties):
    if flume_Conf_Template_file == None:
        print "flume conf template path should not be null"
        return -1
    
    if not os.path.exists(flume_Conf_Template_file):
        print "flume conf template file " + flume_Conf_Template_file + " is not existed"
        return -1
    
    template = open(flume_Conf_Template_file).read()
    template = template.replace(KAFKA_BROKER_LIST_WORD, flumeLogAgentProperties[KAFKA_BROKER_LIST_WORD])
    template = template.replace(KAFKA_LOGGING_TOPIC_WORD, flumeLogAgentProperties[KAFKA_LOGGING_TOPIC_WORD])
    template = template.replace(SERVICE_GROUP_NAME_WORD, flumeLogAgentProperties[SERVICE_GROUP_NAME_WORD])
    template = template.replace(SERVICE_NAME_WORD, flumeLogAgentProperties[SERVICE_NAME_WORD])
    template = template.replace(LOG_FILE_PATH_WORD, flumeLogAgentProperties[LOG_FILE_PATH_WORD])
    
    flumeLogAgentConfTargetPath = flumeLogAgentProperties[FLUME_CONF_TARGET_PATH_KEY]
    flumeLogAgentConfTargetDir = flumeLogAgentConfTargetPath[:flumeLogAgentConfTargetPath.rindex("/")]
    
    if not os.path.exists(flumeLogAgentConfTargetDir):
        os.makedirs(flumeLogAgentConfTargetDir)
    
    if os.path.exists(flumeLogAgentConfTargetPath):
        os.remove(flumeLogAgentConfTargetPath)
        
    flumeLogAgentConfTargetFile = os.open(flumeLogAgentConfTargetPath, os.O_CREAT|os.O_RDWR)
    os.write(flumeLogAgentConfTargetFile, template)
    os.close(flumeLogAgentConfTargetFile)