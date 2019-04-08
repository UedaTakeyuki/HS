#-*- coding:utf-8 -*-
# Copy Right Takeyuki UEDA  © 2019 -

import tornado.websocket
import tornado.web
from tornado import gen

from tornado.log import app_log

import json
'''
Structure

A Screen_WebHander connect with a Screen_WSHandler throug many of id.
Many of Remote_WebHander connect with a Remote_WSHandler throug an id.
Screen_WSHandler and Remote_WSHandler share connections dict; exchange ws connection throug the same id.
'''

TB_handler_classes = ["Screen_WebHander", 
                      "Screen_WSHandler",
                      "Remote_WSHandler", 
                      "Remote_WebHander"]
'''
connections[id]                  id: connection id
               ["screen_socket"] screen side ws connection
               ["remote_socket"] remote side ws connection
              ...

An element is cleated by screen; filled by remote.
'''
connections={}

class Screen_WebHander(tornado.web.RequestHandler):
  route = "/screen"
  def get(self):
    self.render('screen.html')

class Screen_WSHandler(tornado.websocket.WebSocketHandler):
  route = "/screen_connection/(.*)"
  def open(self, id):
    global connections
    app_log.info("open: id =  %s", id)
    self.id = id
    connections[id] = {"screen_socket": self}

  def on_message(self, message):
    global connections
    app_log.info("on_message: message =  %s", message)
    if self.id in connections:
      if "remote_socket" in connections[self.id]:
        connections[self.id]["remote_socket"].write_message(message)  
 
  def on_close(self):
    app_log.info("close:")

class Remote_WSHandler(tornado.websocket.WebSocketHandler):
  route = "/remote_connection/(.*)"
  def open(self, id):
    global connections
    app_log.info("open: id =  %s", id)
    self.id = id
    if id in connections:
      connections[id]["remote_socket"] = self    

  def on_message(self, message):
    global connections
    app_log.info("on_message: message =  %s", message)
    if self.id in connections:
      app_log.info("on_message: id =  %s", self.id)
      if "screen_socket" in connections[self.id]:
        connections[self.id]["screen_socket"].write_message(message)  
 
  def on_close(self):
    app_log.info("close:")

class Remote_WebHander(tornado.web.RequestHandler):
  route = "/remote/(.*)"
  def get(self,id):
    self.render('remote.html', id=id)

