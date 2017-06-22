import os

KAFKA_BROKER_LIST_WORD = "$_kafkaBrokerList_"
KAFKA_LOGGING_TOPIC_WORD = "$_kafkaTopic_"
KAFKA_PARTITION_ID_WORD = "$_kafkaPartitionId_"
SERVICE_GROUP_NAME_WORD = "$_serviceGroupName_"
SERVICE_NAME_WORD = "$_serviceName_"
LOG_FILE_PATH_WORD = "$_logFilePath_"
LOG_FILE_WORD = "$_logFile_"
FLUME_AGENT_SRC_WORD = "$_agentSrc_"
FLUME_AGENT_SRC_INDEX_WORD = "$_srcIndex_"
FLUME_AGENT_INTERCEPTOR_INDEX1_WORD = "$_interceptorIndex1_"
FLUME_AGENT_INTERCEPTOR_INDEX2_WORD = "$_interceptorIndex2_"
FLUME_AGENT_INTERCEPTOR_INDEX3_WORD = "$_interceptorIndex3_"

FLUME_CONF_TARGET_PATH_KEY = "flumeConfTargetPath"
LOG_FILE_LIST_STRING_KEY = "logFiles"
FLUME_CONF_TEMPLATE_KEY = "flumeConfTemplate"
FLUME_CONF_SRC_TEMPLATE_KEY = "flumeConfSrcTemplate"

def buildFlumeLogAgentConf(flumeLogAgentProperties):
    flume_Conf_Template_file = flumeLogAgentProperties[FLUME_CONF_TEMPLATE_KEY]
    if flume_Conf_Template_file == None:
        print "flume conf template path should not be null"
        return -1
    
    flume_Conf_Src_Template_file = flumeLogAgentProperties[FLUME_CONF_SRC_TEMPLATE_KEY]
    if flume_Conf_Src_Template_file == None:
        print "flume conf src template path should not be null"
        return -1 
    
    if not os.path.exists(flume_Conf_Template_file):
        print "flume conf template file " + flume_Conf_Template_file + " is not existed"
        return -1
    
    if not os.path.exists(flume_Conf_Src_Template_file):
        print "flume conf src template file " + flume_Conf_Src_Template_file + " is not existed"
        return -1
    
    logFilesStr = flumeLogAgentProperties[LOG_FILE_LIST_STRING_KEY]
    if logFilesStr == None:
        print "log file str should not be null"
        return -1
    
    srcTemplateTotal = ''
    srcTemplate = open(flume_Conf_Src_Template_file).read()
    srcIndex = 1
    for logFile in logFilesStr.split(','):
        srcTemplateTmp = srcTemplate.replace(LOG_FILE_PATH_WORD, flumeLogAgentProperties[LOG_FILE_PATH_WORD])
        srcTemplateTmp = srcTemplateTmp.replace(LOG_FILE_WORD, logFile)
        srcTemplateTmp = srcTemplateTmp.replace(SERVICE_GROUP_NAME_WORD, flumeLogAgentProperties[SERVICE_GROUP_NAME_WORD])
        srcTemplateTmp = srcTemplateTmp.replace(SERVICE_NAME_WORD, flumeLogAgentProperties[SERVICE_NAME_WORD])
        srcTemplateTmp = srcTemplateTmp.replace(FLUME_AGENT_SRC_INDEX_WORD, str(srcIndex))
        srcTemplateTmp = srcTemplateTmp.replace(FLUME_AGENT_INTERCEPTOR_INDEX1_WORD, str((srcIndex - 1) * 3 + 1 ))
        srcTemplateTmp = srcTemplateTmp.replace(FLUME_AGENT_INTERCEPTOR_INDEX2_WORD, str((srcIndex - 1) * 3 + 2 ))
        srcTemplateTmp = srcTemplateTmp.replace(FLUME_AGENT_INTERCEPTOR_INDEX3_WORD, str((srcIndex - 1) * 3 + 3 ))
        srcTemplateTotal +=  srcTemplateTmp + '\n'
        srcIndex += 1
        
    template = open(flume_Conf_Template_file).read()
    template = template.replace(KAFKA_BROKER_LIST_WORD, flumeLogAgentProperties[KAFKA_BROKER_LIST_WORD])
    template = template.replace(KAFKA_LOGGING_TOPIC_WORD, flumeLogAgentProperties[KAFKA_LOGGING_TOPIC_WORD])
    template = template.replace(KAFKA_PARTITION_ID_WORD, str(flumeLogAgentProperties[KAFKA_PARTITION_ID_WORD]))
    template = template.replace(FLUME_AGENT_SRC_WORD, srcTemplateTotal)
    
    flumeLogAgentConfTargetPath = flumeLogAgentProperties[FLUME_CONF_TARGET_PATH_KEY]
    flumeLogAgentConfTargetDir = flumeLogAgentConfTargetPath[:flumeLogAgentConfTargetPath.rindex("/")]
    
    if not os.path.exists(flumeLogAgentConfTargetDir):
        os.makedirs(flumeLogAgentConfTargetDir)
    
    if os.path.exists(flumeLogAgentConfTargetPath):
        os.remove(flumeLogAgentConfTargetPath)
        
    flumeLogAgentConfTargetFile = os.open(flumeLogAgentConfTargetPath, os.O_CREAT|os.O_RDWR)
    os.write(flumeLogAgentConfTargetFile, template)
    os.close(flumeLogAgentConfTargetFile)