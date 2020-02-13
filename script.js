var etiqueta;
function onloadFcn(){
	etiqueta=document.getElementById("led");
	etiqueta.innerHTML = "led 1";
}

// Create a client instance
  //client = new Paho.MQTT.Client("postman.cloudmqtt.com", 14970);
  
  client = new Paho.MQTT.Client("tailor.cloudmqtt.com", 30148, "web_" + parseInt(Math.random() * 100, 10));

  // set callback handlers
  client.onConnectionLost = onConnectionLost;
  client.onMessageArrived = onMessageArrived;
  var options = {
    useSSL: true,
    userName: "ntdamocq",
    password: "TobTg4zmkQHo",
    onSuccess:onConnect,
    onFailure:doFail
  }

  // connect the client
  client.connect(options);
  topic_tx="led";
  topic_rx="test";
  // called when the client connects
  function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
	
    client.subscribe(topic_rx);
    message = new Paho.MQTT.Message("ll:Hello: CloudMQTT");
    message.destinationName = topic_tx;
    
	
  }

  function doFail(e){
    console.log(e);
	
  }

  // called when the client loses its connection
  function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
      console.log("onConnectionLost:"+responseObject.errorMessage);
    }
  }

  // called when a message arrives
  function onMessageArrived(message) {
    console.log("nuevo Mensaje:"+message.payloadString);
	action(message.payloadString);
  }
  
    // called when a message arrives
  function sendMessage(msg) {
    message = new Paho.MQTT.Message(msg);
    message.destinationName = topic_tx;
    client.send(message);
	
  }

    // called when a message arrives
  function ledon() {
	sendMessage('5000+3000')	
  }
  function ledoff(){
	sendMessage('5000-3000')
  }

  function action(msg) {
	mensaje=msg.split('=')
	if(mensaje[0]=='Viento')
		document.getElementById('sensor_vien').innerHTML=mensaje[1];
	if(mensaje[0]=='Dir')
		document.getElementById('sensor_dire').innerHTML=mensaje[1];
	if(mensaje[0]=='Temperatura')
		document.getElementById('sensor_temp').innerHTML=mensaje[1];
	if(mensaje[0]=='Luz')
		document.getElementById('sensor_luz').innerHTML=mensaje[1];
	if(mensaje[0]=='Humedad')
		document.getElementById('sensor_hume').innerHTML=mensaje[1];
  }