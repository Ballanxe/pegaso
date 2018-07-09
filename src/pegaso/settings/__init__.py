import socket


if socket.gethostname() == "alberto-HP-Pavilion-dv7-Notebook-PC":

	from .local import *

else:

	from .prod import *