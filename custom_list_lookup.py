def custom_list_lookup(customListInput=None, inputDataPath=None, customListHeader=None, **kwargs):
    """
    Given a Custom list, specified data path, and a customer list name. Determine if specified data path value(s) are present in custom list, return a list of true/false values if present, and the entire custom list rows where present.
    
    Args:
        customListInput: This should be passed as formatted text matching a custom list name. Ex: "Authentication Allow List"
        inputDataPath: This should be passed as formatted text matching a valid datapath or list of valid datapaths. Ex: ['artifact:*.cef.fileHashSha256']
        customListHeader: This should be a valid COLUMN HEADER NAME in the custom list that you are referring to. The function will search this header for matching values as specified in 'inputDataPath'
    
    Returns a JSON-serializable object that implements the configured data paths:
        foundInList: List of Booleans
        notFoundInList: List of Booleans
        returnedRows: Dictionary of lists
    """
    ############################ Custom Code Goes Below This Line #################################
 
    import json
    import phantom.rules as phantom
    from collections import OrderedDict
    
    # Variables
    foundInList = []
    lookupList = list()
    notFoundInList = []
    returnedRows = {}
    
    # Functions
    def makeLookupDict(keyField, dictList):
        outputDict = dict()
        
        for row in dictList:
            key = row.get(keyField)
            del row[keyField]
            outputDict.update({key:row})
                
        return(outputDict)
    
    # This gets the name of the custom list provided as an input and stores the custom list's contents
    # in a variable
    
    if isinstance(customListHeader, list):
        if len(customListHeader) > 0:
            customListHeader = str(customListHeader[0]).strip()
        else:
            phantom.debug("Incorrect custom list header")
            customListHeader = "AAAAAAA"
    else:
        customListHeader = str(customListHeader).strip()
     
    if not customListHeader:
        customListHeader = "AAAAAAA"
        
    if isinstance(customListInput, list):
        for items in customListInput:
            success, message, collection = phantom.get_list(items)
    else:
        success, message, collection = phantom.get_list(customListInput)
    
    headers = collection[0]
    valueLists = collection[1:]
    
    
    for num,listTemp in enumerate(valueLists):
        lookupList.append((dict(zip(headers,listTemp))))
        
    #phantom.debug(lookupList)
    
    dictionary = makeLookupDict(customListHeader,lookupList)

    #phantom.debug(dictionary)
    
    #phantom.debug(inputDataPath)
    
    if isinstance(inputDataPath, list):
        for artifacts in inputDataPath:
            if isinstance(artifacts, list) or isinstance(artifacts, dict):
                for item in artifacts:
                        isFound = False
                        for key in dictionary:
                            #phantom.debug('DEBUG: {}'.format(key))
                            if key == item:
                                    #phantom.debug('DEBUG: {}'.format(isFound))
                                    #phantom.debug('DEBUG: key {} found in item {}'.format(key, item))
                                    #phantom.debug('DEBUG: Setting isFound to True')
                                    isFound = True
                                    #phantom.debug(dictionary[key])
                                    returnedRows[key] = dictionary[key]
                                    #phantom.debug(returnedRows)
                        foundInList.append(bool(isFound))
            else:
                isFound = False
                for key in dictionary:
                    if key == str(artifacts):      
                        isFound = True
                        returnedRows[key] = dictionary[key]
                foundInList.append(bool(isFound))      
    else:
        isFound = False
        for key in dictionary:
            #phantom.debug('DEBUG: {}'.format(key))
            if key == str(inputDataPath):
                #phantom.debug('DEBUG: {}'.format(isFound))
                #phantom.debug('DEBUG: key {} found in item {}'.format(key, inputDataPath))
                #phantom.debug('DEBUG: Setting isFound to True')
                isFound = True
                #phantom.debug(dictionary[key])
                returnedRows[key] = dictionary[key]
                #phantom.debug(returnedRows)
        foundInList.append(bool(isFound))
    if isinstance(foundInList, list):
        for b in foundInList:
            notFoundInList.append(not bool(b))
            #phantom.debug("isFound was a list")
            #phantom.debug(foundInList)            
    elif isinstance(foundInList, bool):
        notFoundInList.append(not bool(foundInList))  
        #phantom.debug("isFound was a single bool")
        #phantom.debug(foundInList)
    
            
        
    outputs = {
        'foundInList':foundInList,
        'notFoundInList': notFoundInList,
        'returnedRows':returnedRows
    }
    
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
    return outputs
