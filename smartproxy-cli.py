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

def request( resource, param1='', param2='',  param3='', method='GET', headers={"accept": "application/json",} ):
  url=api_url+resource
  if not param1:
    url_f=url
  else:
    url_f=url+'?'+param1
  if param2:
    url_f=url_f+'&'+param2
  if param3:
    url_f=url_f+'&'+param3
  if (args.debug):
    print(url_f)
  response = requests.request(
    method,
    url_f,
    headers=headers,
  )
  if not (args.noverbose) or (args.debug):
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(',', ': ')))
  return(response.json())
#############################################################################
#############################################################################
parser = argparse.ArgumentParser(description='https://github.com/osgpcq/smartproxy-cli-py',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client',               default='exo',       help='Config file selection')
parser.add_argument('--endpoints',            action='store_true', help='Endpoints list')
parser.add_argument('--endpoints_type',       action='store',      help='Endpoints_type', choices=['random', 'sticky'])
parser.add_argument('--subscriptions',        action='store_true', help='List subscriptions')
parser.add_argument('--traffic',              action='store_true', help='List traffic --users needed')
parser.add_argument('--users',                action='store_true', help='List usres')
parser.add_argument('--service_type',         action='store',      help='Choose service', choices=['residential_proxies', 'shared_proxies'])
parser.add_argument('--debug',                action='store_true', help='Debug information')
parser.add_argument('--noverbose',            action='store_true', default=False, help='Verbose')
args = parser.parse_args()

config_file='./smartproxy-'+args.client+'.conf'
if os.path.isfile(config_file):
  parser = ConfigParser()
  parser.read('./smartproxy-'+args.client+'.conf', encoding='utf-8')
  api_key = 'api-key='+parser.get('smartproxy', 'api_key')
else:
  sys.exit('Configuration file not found!')

if (args.endpoints):
  endpoints=request( resource='endpoints')
if (args.endpoints_type):
  endpoints_type=request( resource='endpoints/'+(args.endpoints_type))

if (args.subscriptions):
  subscriptions=request( resource='subscriptions', param1=api_key)
if (args.users):
  if not (args.service_type):
    users=request( resource='sub-users', param1=api_key )
  else:
    users=request( resource='sub-users', param1='service_type='+(args.service_type), param2=api_key )
  if (args.traffic):
    table = []
    for user in users:
      traffic=request( resource='sub-users/'+str(user['id'])+'/traffic', param1='type=month', param2=api_key )
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
