import json
import urllib, urllib2

def run_query(search_terms):
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'
    
    results_per_page = 10
    results_offset = 0 
    
    #Wrap the query terms
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query) #Quote the string in order to send safe strings
    
    #Construct the request URL latter part and 
    #Set the format of the response to JSON format
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        results_offset,
        query)
    
    #Authentication Setup
    username = '' #Must be a blank str
    bing_api_key = "pNeTEboL7JVaaiKVow0XEA5H9SguyuKulhB/cbauoZI"
    
    #Create the 'password manager' to deal with the authentication
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, bing_api_key)

    results = []
    
    try:
        #Connection preparation
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        #Connect to server
        response = urllib2.urlopen(search_url).read()
        
        #Convert the string to a python dictionary
        json_response = json.loads(response)
        
        #Loop throught the results
        for result in json_response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']})
                
    except urllib2.URLError, e:
        print "Error when querying the Bing API: ", e
        
    return results
    