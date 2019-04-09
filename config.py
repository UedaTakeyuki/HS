#-*- coding:utf-8 -*-
# Copy Right Takeyuki UEDA  © 2019 - All rights reserved.

#protocol = "wss:"
protocol = "ws:"

data_dir = "/etc/letsencrypt/live/.com/"
additional_module_paths    = ["handler"] 
#tb_handlers    = ["screen", "ws_exchange"]
tb_handlers    = ["screen"]
templates_path = "handler/templates"

log_file_prefix = "/var/log/tornado_base/tb.log"
logging = "debug"
