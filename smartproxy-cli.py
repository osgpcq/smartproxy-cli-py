#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################################################
#############################################################################
#############################################################################
# pip3 install tabulate --user
#
# https://help.smartproxy.com/reference/get-api-key-for-authentication
#############################################################################
import requests
import json
import argparse
import sys, os.path
from http.client import HTTPConnection  # Debug mode
from configparser import ConfigParser
from tabulate import tabulate

api_ver = 'v2'
api_url = 'https://api.smartproxy.com/'+api_ver+'/'
#############################################################################
def request( method='GET', resource='' , auth='', headers={}, params='', data='' ):
  # data:   POST, PUT, ...
  # params: GET, ...
  url=api_url+resource
  headers.update({'accept': 'application/json'})
  if (args.verbose) or (args.debug):
    print(url)
    if (args.debug):
      # print statements from `http.client.HTTPConnection` to console/stdout
      HTTPConnection.debuglevel=1
  response=requests.request(
    method,
    api_url+resource,
    auth=auth,
    headers=headers,
    params=params,
    data=data
  )
  if (args.verbose) or (args.debug):
    print('Status code: '+str(response.status_code))
  if (args.debug):
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(',', ': ')))
  return(response.json())
#############################################################################
#############################################################################
parser = argparse.ArgumentParser(description='https://github.com/osgpcq/smartproxy-cli-py',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client',               default='exo',       help='Choose the API key')
parser.add_argument('--endpoints',            action='store_true', help='List Endpoints')
parser.add_argument('--endpoints_type',       action='store',      help='Chooe endpoints_type', choices=['random', 'sticky'])
parser.add_argument('--subscriptions',        action='store_true', help='List subscriptions')
parser.add_argument('--users',                action='store_true', help='List users')
parser.add_argument('--service_type',         action='store',      help='Choose service', choices=['residential_proxies', 'shared_proxies'])
parser.add_argument('--traffic',              action='store_true', help='List traffic --users needed')
parser.add_argument('--noheaders',            action='store_true', help='No headers in the output')
parser.add_argument('--debug',                action='store_true', help='Debug information')
#parser.add_argument('--verbose',              action='store_true', default=True, help='Verbose')
parser.add_argument('--verbose',              action='store_true', default=False, help='Verbose')
args = parser.parse_args()

config_file='./config.conf'
if os.path.isfile(config_file):
  parser = ConfigParser(interpolation=None)
  parser.read(config_file, encoding='utf-8')
  api_key = parser.get('smartproxy', 'api_key_'+args.client)
else:
  sys.exit('Configuration file not found!')

if (args.endpoints):
  endpoints=request( resource='endpoints' )
if (args.endpoints_type):
  endpoints_type=request( resource='endpoints/'+args.endpoints_type )

if (args.subscriptions):
  subscriptions=request( resource='subscriptions', params={ 'api-key': api_key } )
if (args.users):
  if not (args.service_type):
    users=request( resource='sub-users', params={ 'api-key': api_key} )
  else:
    users=request( resource='sub-users', params={ 'service_type': args.service_type, 'api-key': api_key } )
  if (args.noheaders):
    print(tabulate(sorted(users, key=lambda item: (item['username']) ), tablefmt='plain'))
  else:
    print(tabulate(sorted(users, key=lambda item: (item['username']) ), tablefmt='rounded_outline', headers='keys'))
  if (args.traffic):
    table = []
    for user in users:
      traffic=request( resource='sub-users/'+str(user['id'])+'/traffic', params={ 'type': 'month', 'api-key': api_key } )
      if 'traffic' in traffic:
        table.append([
          user['username'],
          traffic['traffic'],
          traffic['traffic_rx'],
          traffic['traffic_tx'],
        ])
    if (args.noheaders):
      print(tabulate(sorted(table, key=lambda item: (item[2]), reverse=True), tablefmt='plain'))
    else:
      print(tabulate(sorted(table, key=lambda item: (item[2]), reverse=True), tablefmt='rounded_outline', headers=['username', 'traffic', 'traffic_rx', 'traffic_tx']))
#############################################################################
#############################################################################
#############################################################################
