import socket
# print(socket.gethostname())
if socket.gethostname()=="AMOC":
    from .local import *
else:
    from .production import *