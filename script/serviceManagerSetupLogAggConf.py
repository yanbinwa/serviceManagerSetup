import os

KAFKA_BROKER_LIST_WORD = "$_kafkaBrokerList_"
KAFKA_LOGGING_TOPIC_WORD = "$_kafkaTopic_"
LOG_FILE_ROOT_PATH_WORD = "$_logFileRootPath_"
FLUME_CONF_TARGET_PATH_KEY = "flumeConfTargetPath"

def buildFlumeLogAggConf(flume_Conf_Template_file, flumeLogAggProperties):
    
    if flume_Conf_Template_file == None:
        print "flume conf template path should not be null"
        return -1
    
    if not os.path.exists(flume_Conf_Template_file):
        print "flume conf template file " + flume_Conf_Template_file + " is not existed"
        return -1
        
    template = open(flume_Conf_Template_file).read()
    template = template.replace(KAFKA_BROKER_LIST_WORD, flumeLogAggProperties[KAFKA_BROKER_LIST_WORD])
    template = template.replace(KAFKA_LOGGING_TOPIC_WORD, flumeLogAggProperties[KAFKA_LOGGING_TOPIC_WORD])
    template = template.replace(LOG_FILE_ROOT_PATH_WORD, flumeLogAggProperties[LOG_FILE_ROOT_PATH_WORD])
    
    flumeLogAggConfTargetPath = flumeLogAggProperties[FLUME_CONF_TARGET_PATH_KEY]
    flumeLogAggConfTargetDir = flumeLogAggConfTargetPath[:flumeLogAggConfTargetPath.rindex("/")]
        
    if not os.path.exists(flumeLogAggConfTargetDir):
        os.makedirs(flumeLogAggConfTargetDir)
    
    if os.path.exists(flumeLogAggConfTargetPath):
        os.remove(flumeLogAggConfTargetPath)
        
    flumeLogAggConfTargetFile = os.open(flumeLogAggConfTargetPath, os.O_CREAT|os.O_RDWR)
    os.write(flumeLogAggConfTargetFile, template)
    os.close(flumeLogAggConfTargetFile)