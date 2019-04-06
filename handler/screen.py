#-*- coding:utf-8 -*-
# Copy Right Takeyuki UEDA  © 2018 -

import tornado.websocket
import tornado.web
from tornado import gen

from tornado.log import app_log

import datetime
'''
A global variable of dictionaly "connections" should be added at outside of this module,
 and share between rhizosphere main function.
'''

TB_handler_classes = ["ScreenHander", "ButtonHandler"]


class ScreenHander(tornado.web.RequestHandler):
  route = "/"
  def get(self):
    self.render('index.html', route=datetime.datetime.today())

class ButtonHandler(tornado.web.RequestHandler):
  route = "/button"
  def get(self):
    self.set_header('Content-Type', 'application/json; charset=UTF-8')
    self.finish({'message': 'ok'})

