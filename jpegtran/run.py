#!/usr/bin/env python
import os



# os.system('cmd /k')
for i in os.listdir('old'):
	os.system('jpegtran.exe -copy none -optimize -perfect old\%s new\%s' % (i, i) )
	print 'ok ------------ %s' % i
