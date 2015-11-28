# this is basically a beanstalk shim
# beanstalk imports application.py and then does application.run()
# what this also means is that application.py imports server.py
# so the __name__ = "__main__" in server.py isn't true anymore
# I turn on logging only when my app is being run by application.py
# to avoid double logging
from server import app as application
