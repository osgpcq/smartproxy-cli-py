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
from configparser import ConfigParser
from tabulate import tabulate

api_ver = 'v2'
api_url = 'https://api.smartproxy.com/'+api_ver+'/'

def request( method='GET', resource='', params='', headers={"accept": "application/json",} ):
  url=api_url+resource
  if (args.debug):
    print(url)
    # print statements from `http.client.HTTPConnection` to console/stdout
    #HTTPConnection.debuglevel = 1
  if method=='POST':
    response = requests.post(
      api_url+resource,
      headers=headers,
      data=params
    )
  elif method=='GET':
    if params:
      urlp=''
      for param in params:
        if urlp=='':
          urlp=urlp+param
        else:
          urlp=urlp+'&'+param
      url=url+'?'+urlp
    response = requests.get(
      url,
      headers=headers,
    )
  if not (args.noverbose) or (args.debug):
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
parser.add_argument('--traffic',              action='store_true', help='List traffic --users needed')
parser.add_argument('--users',                action='store_true', help='List users')
parser.add_argument('--service_type',         action='store',      help='Choose service', choices=['residential_proxies', 'shared_proxies'])
parser.add_argument('--debug',                action='store_true', help='Debug information')
parser.add_argument('--noverbose',            action='store_true', default=False, help='Verbose')
args = parser.parse_args()

config_file='./config.conf'
if os.path.isfile(config_file):
  parser = ConfigParser(interpolation=None)
  parser.read(config_file, encoding='utf-8')
  api_key = 'api-key='+parser.get('smartproxy', 'api_key_'+args.client)
else:
  sys.exit('Configuration file not found!')

if (args.endpoints):
  endpoints=request( resource='endpoints')
if (args.endpoints_type):
  endpoints_type=request( resource='endpoints/'+(args.endpoints_type))

if (args.subscriptions):
  subscriptions=request( resource='subscriptions', params={ api_key } )
if (args.users):
  if not (args.service_type):
    users=request( resource='sub-users', params={ api_key} )
  else:
    users=request( resource='sub-users', params={ 'service_type='+(args.service_type), api_key } )
  table = []
  for user in users:
    table.append([
      user['username'],
    ]),
  print(tabulate(sorted(table), headers=['username']))
  if (args.traffic):
    table = []
    for user in users:
      traffic=request( resource='sub-users/'+str(user['id'])+'/traffic', params={ 'type=month', api_key } )
      if 'traffic' in traffic:
        table.append([
          user['username'],
          traffic['traffic'],
          traffic['traffic_rx'],
          traffic['traffic_tx'],
        ])
    print(tabulate(sorted(table, key=lambda item: (item[2]), reverse=True), headers=['username', 'traffic', 'traffic_rx', 'traffic_tx']))
#############################################################################
#############################################################################
#############################################################################
