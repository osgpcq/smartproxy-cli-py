# smartproxy-cli-py
SmartProxy Python command-line interface.

Extract informations from SmartProxy.


# Usage
```
./smartproxy-cli.py --help
options:
  -h, --help            show this help message and exit
  --client CLIENT       Choose the API key (default: exo)
  --endpoints           List Endpoints (default: False)
  --endpoints_type {random,sticky}
                        Chooe endpoints_type (default: None)
  --subscriptions       List subscriptions (default: False)
  --users               List users (default: False)
  --service_type {residential_proxies,shared_proxies}
                        Choose service (default: None)
  --traffic             List traffic --users needed (default: False)
  --noheaders           No headers in the output (default: False)
  --debug               Debug information (default: False)
  --verbose             Verbose (default: False)


./smartproxy-cli.py --users

./smartproxy-cli.py --client XxX --users --traffic
╭──────────┬───────────┬──────────────┬──────────────╮
│ username │   traffic │   traffic_rx │   traffic_tx │
├──────────┼───────────┼──────────────┼──────────────┤
│ user01   │    473.36 │       459.39 │        13.97 │
│ user02   │      0    │         0    │         0    │
│ ...      │           │              │              │
╰──────────┴───────────┴──────────────┴──────────────╯

./smartproxy-cli.py --endpoints --debug
./smartproxy-cli.py --endpoints --endpoints_type random --debug | more
[
  {
    "hostname": "gate.smartproxy.com",
    "location": "Random",
    "port_range": "7000"
  },
  {
  ...
```


# History
Still in quick & dirty dev phase!
