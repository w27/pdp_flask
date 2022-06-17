from lib_sqlconnect import *

ex = SQLConnect()

print(ex.get(Course, "name", "Python 100", False))