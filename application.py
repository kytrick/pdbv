# this is basically a beanstalk shim
# beanstalk imports application.py and then does application.run()

from server import app as application
