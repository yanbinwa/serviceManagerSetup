#import yaml
import os

JAVA_UTIL_HASHMAP_KEY = '!java.util.HashMap'
NET_SF_JSON_JSONOBJECT_KEY = '!net.sf.json.JSONObject'

if __name__ == "__main__":

#     path = "/User/yanbinwa/ppm/message.txt"
#     
#     path1 = "/User/yanbinwa/ppm/message.txt"
#     
#     map1 = {}
#     map1['wyb'] = 1
#     print map1.has_key('zcl')

#     logFiles = 'message,console'
#     logFileList = logFiles.split(',')
#     for logFile in logFileList:
#         print logFile

#     testYaml = yaml.safe_load(open('/Users/yanbinwa/Documents/workspace/springboot/serviceManager/serviceManagerCommon/src/test/file/YamlUtilTest.yaml'))
#     print testYaml
    
    manifestFile = '/tmp/manifest.yml'
    template = open(manifestFile).read()
    template = template.replace(JAVA_UTIL_HASHMAP_KEY, '')
    template = template.replace(NET_SF_JSON_JSONOBJECT_KEY, '')
    manifestFileTmp = os.open(manifestFile, os.O_CREAT|os.O_RDWR)
    os.write(manifestFileTmp, template)
    os.close(manifestFileTmp)