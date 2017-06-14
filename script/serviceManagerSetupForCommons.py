import serviceManagerSetupForCommonsFlume

COMMON_FLUME_KEY = "flume"

def setupAnsibleCommons(rootPath, commons):
    if commons == None:
        print "No common service, just return"
        return
    
    for commonServiceKey in commons.keys():
        commonService = commons[commonServiceKey]
        if commonService == None:
            print "commonService should not be null " + commonServiceKey
            continue
        
        if commonServiceKey == COMMON_FLUME_KEY:
            serviceManagerSetupForCommonsFlume.setupAnsibleFlume(rootPath, commonService)
        else:
            print "Dose not support " + commonServiceKey