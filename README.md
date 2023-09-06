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
  --traffic             List traffic --users needed (default: False)
  --users               List users (default: False)
  --service_type {residential_proxies,shared_proxies}
                        Choose service (default: None)
  --debug               Debug information (default: False)
  --noverbose           Verbose (default: False)


./smartproxy-cli.py --client XxX --users --traffic --noverbose
username                 traffic    traffic_rx    traffic_tx
---------------------  ---------  ------------  ------------
titi01                      1.44          1.4           0.04
titi02                      0.62          0.61          0.01
titi03                      0.62          0.6           0.02
titi04                      0.35          0.34          0.01
titi05                      0.25          0.24          0.01
titi06                      0.2           0.19          0.01
titi07                      0.15          0.15          0
titi08                      0.11          0.11          0
titi09                      0.1           0.09          0.01
titi10                      0.07          0.07          0
titi11                      0.06          0.06          0
titi12                      0.04          0.04          0
titi13                      0.03          0.03          0
titi14                      0.02          0.02          0
titi15                      0.02          0.02          0
titi16                      0.02          0.02          0
titi17                      0.02          0.02          0
titi18                      0.02          0.02          0
titi19                      0.01          0.01          0
titi20                      0             0             0
titi21                      0             0             0
titi22                      0             0             0
...

./smartproxy-cli.py --endpoints --endpoints_type random | more
[
  {
    "hostname": "gate.smartproxy.com",
    "location": "Random",
    "port_range": "7000"
  },
  {
    "hostname": "us.smartproxy.com",
    "location": "USA",
    "port_range": "10000"
  },
  {
    "hostname": "ca.smartproxy.com",
    "location": "Canada",
    "port_range": "20000"
  },
...
```


# History
Still in quick & dirty dev phase!
