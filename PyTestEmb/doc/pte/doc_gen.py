# -*- coding: UTF-8 -*-


import pytestemb



data = ""

data += "<b>PYTESTEMB API</b>\n\n"
data += "<b>Version : %s</b>\n\n" % pytestemb.VERSION_STRING


for f in pytestemb.__api__:
    data += "<b>%s</b>\n" % f.__name__
    data += "%s\n\n" % f.__doc__
    #, f.__doc__
    
print data

data = data.replace("\n", "<br />")

html = """<!DOCTYPE html>
<html>
  <head>
    <title>Hello HTML</title>
  </head>
  <body>
    <p>%s</p>
  </body>
</html>""" % data


filename = "pytestemb_api_%s.html" % pytestemb.VERSION_STRING.replace(".", "_")

open(filename,"w").write(html)




