#!/usr/bin/python
# James Tobat
# Last Updated: 7/15/14
# Description: Introductory script that will print out the key and values
# of all form data submitted to this script. A simple little test to see how
# wsgi works.

import cgi

def application(environ, start_response):
   status = '200 OK'
   response_headers = [('Content-type', 'text/plain')]
   form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
   msg = ""
   # Iterates through all form data and prints out the corresponding value
   # for each key.
   for key in form_data:
     value = form_data.getvalue(key)
     msg += "The key is %s and the value is %s \n" % (key, value)
   start_response(status, response_headers)
   return [msg]

