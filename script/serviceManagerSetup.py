import serviceManagerSetupForAnsibleHost
import serviceManagerSetupForAnsibleMainScript
import serviceManagerSetupForDocker
import serviceManagerSetupForZookeeper
import serviceManagerSetupForOrchestration
import serviceManagerSetupForCollection
import serviceManagerSetupForKafka
import serviceManagerSetupForCache
import serviceManagerSetupForLogging
import serviceManagerSetupForRedis
import serviceManagerSetupForCommons
import serviceManagerSetupForAggregation
import serviceManagerSetupForConfig
import serviceManagerSetupForDeploy

import yaml
import sys
import os

ROOT_TARGET_PATH_KEY = 'root_path'
ANSIBLE_HOST_PATH_KEY = 'ansible_host'
ANSIBLE_MAIN_PATH_KEY = 'ansible_main'
COMPONENT_KEY = 'components'
COMMON_KEY = 'commons'
DOCKER_CONTAINER_PATH_KEY = 'docker_container'
BASEINOF_KEY = 'baseInfo'

ZOOKEEPER_KEY = 'zookeeper'
ORCHESTRATION_KEY = 'orchestration'
COLLECTION_KEY = 'collection'
KAFKA_KEY = 'kafka'
CACHE_KEY = 'cache'
LOGGING_KEY = 'logging'
REDIS_KEY = 'redis'
AGGREGATION_KEY = 'aggregation'
CONFIG_KEY = 'config'
DEPLOY_KEY = 'deploy'

JAVA_UTIL_HASHMAP_KEY = '!java.util.HashMap'
NET_SF_JSON_JSONOBJECT_KEY = '!net.sf.json.JSONObject'

class serviceManagerSetup:

    def __init__(self):
        
        if len(sys.argv) < 2:
            print "Should input the manifest file path"
            exit(-1)
            
        self.manifestFile = sys.argv[1]   
        self.adjustYamlFile()
        
        self.manifest = yaml.safe_load(open(self.manifestFile))
        
        self.baseInfo = self.manifest[BASEINOF_KEY];
        self.rootPath = self.baseInfo[ROOT_TARGET_PATH_KEY]
        self.ansibleHostPath = self.rootPath + self.baseInfo[ANSIBLE_HOST_PATH_KEY]
        
        self.components = self.manifest[COMPONENT_KEY]
        if self.components == None:
            print "The components should not be Null"
            exit(-1)
           
        if self.manifest.has_key(COMMON_KEY):    
            self.commons = self.manifest[COMMON_KEY]
                
        serviceManagerSetupForAnsibleHost.setupAnsibleHost(self.ansibleHostPath, self.components, self.commons)
        
        self.dockerContainer = self.rootPath + self.baseInfo[DOCKER_CONTAINER_PATH_KEY]
        serviceManagerSetupForDocker.setupDockerContainer(self.dockerContainer, self.components)
        
        self.ansibleMainPath = self.rootPath + self.baseInfo[ANSIBLE_MAIN_PATH_KEY]
        serviceManagerSetupForAnsibleMainScript.setupAnsibleMain(self.rootPath, self.ansibleMainPath, self.components, self.commons)
          
        if self.components.has_key(ZOOKEEPER_KEY):
            self.zookeepers = self.components[ZOOKEEPER_KEY]
            serviceManagerSetupForZookeeper.setupAnsibleZookeeper(self.rootPath, self.zookeepers)
        
        if self.components.has_key(ORCHESTRATION_KEY):
            self.orchestrations = self.components[ORCHESTRATION_KEY]
            serviceManagerSetupForOrchestration.setupAnsibleOrchestration(self.rootPath, self.orchestrations)
        
        if self.components.has_key(COLLECTION_KEY):
            self.collections = self.components[COLLECTION_KEY]
            serviceManagerSetupForCollection.setupAnsibleCollection(self.rootPath, self.collections)
        
        if self.components.has_key(KAFKA_KEY):
            self.kafkas = self.components[KAFKA_KEY]
            serviceManagerSetupForKafka.setupAnsibleKafka(self.rootPath, self.kafkas)
        
        if self.components.has_key(CACHE_KEY):
            self.caches = self.components[CACHE_KEY]
            serviceManagerSetupForCache.setupAnsibleCache(self.rootPath, self.caches)
        
        if self.components.has_key(AGGREGATION_KEY):
            self.aggregations = self.components[AGGREGATION_KEY]
            serviceManagerSetupForAggregation.setupAnsibleAggregation(self.rootPath, self.aggregations)
        
        if self.components.has_key(LOGGING_KEY):
            self.logging = self.components[LOGGING_KEY]
            serviceManagerSetupForLogging.setupAnsibleLogging(self.rootPath, self.logging)
        
        if self.components.has_key(REDIS_KEY):
            self.rediss = self.components[REDIS_KEY]
            serviceManagerSetupForRedis.setupAnsibleRedis(self.rootPath, self.rediss)
        
        if self.components.has_key(CONFIG_KEY):
            self.configs = self.components[CONFIG_KEY]
            serviceManagerSetupForConfig.setupAnsibleConfig(self.rootPath, self.configs)
        
        if self.components.has_key(DEPLOY_KEY):
            self.deploys = self.components[DEPLOY_KEY]
            serviceManagerSetupForDeploy.setupAnsibleDeploy(self.rootPath, self.deploys)
        
        serviceManagerSetupForCommons.setupAnsibleCommons(self.rootPath, self.commons)
        
    def adjustYamlFile(self):
        template = open(self.manifestFile).read()
        os.remove(self.manifestFile)
        template = template.replace(JAVA_UTIL_HASHMAP_KEY, '')
        template = template.replace(NET_SF_JSON_JSONOBJECT_KEY, '')
        manifestFileTmp = os.open(self.manifestFile, os.O_CREAT|os.O_RDWR)
        os.write(manifestFileTmp, template)
        os.close(manifestFileTmp)

# Start of the python invocation, the argv is manifest file
if __name__ == "__main__":
    setup = serviceManagerSetup()