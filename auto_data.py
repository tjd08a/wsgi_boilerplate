# James Tobat
# Last Updated: 7/16/14
# Description: Script that finds all the unique terms of
# a given JSON attribute that is located in the Open Catalog
import cgi
import json
import sys
import glob
from collections import OrderedDict

home_dir = "/home/jtobat/"
data_dir = home_dir+"test/open-catalog-generator/"
program_path = data_dir + "active_content.json"
script_path = data_dir + "scripts"
catalog = data_dir + "darpa_open_catalog"
schemas_path = catalog + "/00-schema-examples.json"
sys.path.insert(0, script_path)

def findTerms(json_record, field_list, term_list):
  for field in field_list:
    if field in json_record:
        if isinstance(json_record[field], list):
          for term in json_record[field]:
            if not term in term_list[field] and term != "":
              term_list[field].append(term)
        else:
          term = json_record[field]
          if not term in term_list[field] and term !="":
            term_list[field].append(term)
  return term_list

def getProgramNames (path):
  nameList = []
  json_content = openJSON(path)
  for record in json_content:
    nameList.append(record['Program Name'])
  return nameList

def retrieveFieldNames(fieldList, schemaList):
  openPubs = False
  openPrograms = False
  openSoftware = False
  term_list = {}
  for field in fieldList:
    term_list[field] = []
    for schema in schemaList:
      if field in schema['Schema'][0]:
        if schema['Type'] == "Program":
          openPrograms = True
        elif schema['Type'] == "Publication":
          openPubs = True
        else:
          openSoftware = True

  search_files = []
  if openPrograms:
    search_path = catalog + "/*-program.json"
    search_files.extend(glob.glob(search_path))
    
  if openPubs:
    search_path = catalog + "/*-pubs.json"
    search_files.extend(glob.glob(search_path))

  if openSoftware:
    search_path = catalog + "/*-software.json"
    search_files.extend(glob.glob(search_path))

  for doc in search_files:
    json_data = openJSON(doc)

    if isinstance(json_data, list):
      for record in json_data:
        term_list = findTerms(record, fieldList, term_list)
    else:
      term_list = findTerms(json_data, fieldList, term_list)

  return term_list

def openJSON(file_path):
  json_file = open(file_path, 'r')
  try:
    json_content = json.load(json_file, object_pairs_hook=OrderedDict)
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % file_path
    print " Details: %s" % str(e)
    sys.exit(1)

  return json_content

def application(environ, start_response):
   server_response = {}
   request_body = environ['wsgi.input'].read()
   fieldList = json.loads(request_body)
   status = '200 OK'
   response_headers = [('Content-type', 'application/json')]
   start_response(status, response_headers)
   server_response['Schemas'] = openJSON(schemas_path)
   server_response['Program_Names'] = getProgramNames(program_path)
   server_response['Auto_Data'] = retrieveFieldNames(fieldList['autoFields'], server_response['Schemas'])
   json_response = json.dumps(server_response)

   return [json_response]
