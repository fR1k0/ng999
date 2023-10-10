var source = new EventSource("http://localhost:8080/rest/events?topics=smarthome/items/*/state");
source.onmessage = function(ev) { 
  console.log("Received local " + JSON.parse(ev.data));
	
/*
					topic=json.loads(event.data)['topic']
					topic = topic.replace("smarthome/items/","")
					topic = topic.replace("/statechanged","")				
					state=json.loads(json.loads(event.data)['payload'])				
					x = {
					"name": topic,
					"type": state['type'],
					"state": state['value']
					}

*/
  
};

