import httplib
import json
import time

def log_debug(msg):
    print msg
    time.sleep(1)
class RestApiTest():

    def __init__(self, server, port):
        self.server = server
        self.port = port
            
    #List of all switch DPIDs connected to the controller 
    def get_switches(self):
        fl_uri="http://"+self.server+":"+str(self.port)+"/wm/core/controller/switches/json"
        ret=self.rest_call(fl_uri)
        return ret
        
    #Compose aggregate stats
    #statType: port, queue, flow, aggregate, desc, table, features, host	    
    def get_aggregate_stats(self,statType):
        #compose REST call uri
        fl_uri="http://"+self.server+":"+str(self.port)+"/wm/core/switch/all/"+statType+"/json"
        ret=self.rest_call(fl_uri)
        return ret
        
    #Retrieve per switch stats     
    #switchId: Valid Switch DPID (XX:XX:XX:XX:XX:XX:XX:XX)
    #statType: port, queue, flow, aggregate, desc, table, features, host     
    def get_switch_statistics(self,switchId,statType):
        fl_uri="http://"+self.server+":"+str(self.port)+"/wm/core/switch/"+switchId+"/"+statType+"/json"
        ret=self.rest_call(fl_uri)
        return ret
        
    #List of globat traffic counters in the controler     
    #/wm/core/counter/<counterTitle>/json 
    # all or
    #counter in form DPID_Port#OFEventL3/4_Type
    def get_global_traffic_counters( self,counterTitle):
        fl_uri="http://"+self.server+":"+str(self.port)+"/wm/core/counter/"+counterTitle+"/json" 
        ret=self.rest_call(fl_uri)
        return ret
        
    def get_switch_traffic_counters(self,switchId,counterName):
        fl_uri="http://"+self.server+":"+str(self.port)+"/wm/core/counter/"+switchId+"/"+counterName+"/json"          
        ret=self.rest_call(fl_uri)
        return ret

    #/wm/topology/links/json      
    #List all the inter-switch links connected to the same controller.
    def get_topology_links(self):
        fl_uri="http://"+self.server+":"+str(self.port)+"/wm/topology/links/json"
        ret=self.rest_call(fl_uri)
        return ret
         
    def rest_call(self, path):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        #body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, self.port)
        conn.request('GET', path, "", headers)
        response = conn.getresponse()
        res = (response.status, response.reason, response.read())        
        conn.close()
        
        if(res[0]==200):
            response_dict=json.loads(res[2])
            return response_dict            
        else:
            print "Rest API invalid call, status: %d, reason: %s" % (res[0],res[1])
            return None
	
class StaticFlowPusher(object):

    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticflowentrypusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())        
        conn.close()
        return ret
