#-*- coding:utf-8 -*-
# Copy Right Takeyuki UEDA  © 2019 - All rights reserved.
'''
Tornado Base:

A framework of tornado for modularity.
'''

import tornado.ioloop
import tornado.web
from tornado.options import define, options
import ssl
import os
import sys
import pprint
import importlib
import screen

if __name__ == "__main__":
# options
    define("protocol",               default="wss:", help="ws: or wss:(default)")
    define("port",                   default=8888, help="listening port", type=int)    
    define("data_dir",               default="", help="cert file path for running with ssl")
    define("cert_file",              default="cert.pem", help="cert file name for running with ssl")
    define("privkey_file",           default="privkey.pem", help="privkey file name for running with ssl")
    define("config_file",            default="",         help="config file path")
    define("static_path",            default="./",       help="[mandatory] handler class name of rhizome")

    options.parse_command_line()

    '''
    The priority of Option file

    1. options.config_file
    2. ./config.py
    '''
    if os.path.exists('./config.py'):
        options.parse_config_file('./config.py', final=False)
    if options.config_file:
        options.parse_config_file(options.config_file, final=False)

    '''
    command line is the first priority
    '''
    options.parse_command_line()


# app
    BASE_DIR = os.path.dirname(__file__)

    app_params = {}
    app_params["handler"] = [("/",                      screen.Screen_WebHander),
                             ("/screen_connection/(.*)",screen.Screen_WSHandler),
                             ("/remote_connection/(.*)",screen.Remote_WSHandler),
                             ("/remote/(.*)",           screen.Remote_WebHander)
                             ]
    app_params["static_path"]   = os.path.join(BASE_DIR, options.static_path)


    app = tornado.web.Application(
        app_params["handler"], 
        template_path = ".",
        static_path   = app_params["static_path"],
    )

    if options.protocol == "ws:":
        http_server = tornado.httpserver.HTTPServer(app)
    else:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        data_dir = options.data_dir
        ssl_ctx.load_cert_chain(os.path.join(data_dir, options.cert_file),
                                os.path.join(data_dir, options.privkey_file))
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)

    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()