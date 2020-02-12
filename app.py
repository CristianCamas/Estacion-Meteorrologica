#!/usr/bin/python

try:
	from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
except:
	from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
try:
	from urlparse import urlparse
	from urlparse import urlparse, parse_qs
except:
	from urllib.parse import urlparse, parse_qs

import os
port = int(os.environ.get("PORT", 5000))	
PORT_NUMBER = port



#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		print(self.path.split('/')[-1])
		nombre=self.path.split('/')[-1]
		print('hola como estas')
		datos=''
		if self.path=="/":  #127.0.0.1:5000/
			nombre="estacion_meteorologica.html" #127.0.0.1:5000/index.html
		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if nombre.endswith(".html"):
				mimetype='text/html'
				f=open(nombre)
				datos=f.read()
				f.close()
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				f=open(nombre)
				datos=f.read()
				f.close()
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				f=open(nombre)
				datos=f.read()
				f.close()
				sendReply = True
			if sendReply == True:
				#Open the static file requested and send it
				#f = open(curdir + sep + self.path,'r') 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				
				try:
					self.wfile.write(datos)
				except:
					self.wfile.write(bytes(datos, 'UTF-8'))
				
			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
	
