# vstvgo-homeassistant-dashboard

The following repo was created for watching UStvgo channels via home assistant dashboard, broadcasting to google chromecast. 

Assuming you have a Home Assistant Core (python server) running 
https://www.home-assistant.io/installation/

and you are managing dashboards using YAML files

this project utilizes https://github.com/benmoose39/ustvgo_to_m3u project to get the .m3u streaming files provided by ustvgo.tv, these streams are valid only for ~4 hours and need to be refreshed

when managing the HA dashboards using YAML - no restart is required when refreshing the links in the dashboard.

steps to run:
go to your .homeassistant folder (where the configuration.yaml is)
and run:

```
git clone https://github.com/yishait/ustvgo-homeassistant-dashboard.git
```

once completed, setup the environment by running the setup.sh file
```
source setup.sh
```
inside scripts folder

add your rooms and the devices used in them to the settings.yaml file:
dashboard_settings:
  room1: 
    devices: 
      - device_1
  room2: 
    devices:
      - device_2

if they dont exist - the script will add them to your configuration.yaml used to run Home-assistant 

once all setup is completed you should see the new alias: channel_dispatcher
and you will be able to run:
```
channel_dispatcher 
```
to create the channel cards and the dashboards according to the setup in settings.yaml

##additional vars:

```
channel_dispatcher --cron true --cron_min X
```
will trigger an exacution every X minutes (when no cron_min is provided the default is 210 min=3.5 hours).

```
channel_dispatcher --log INFO
```
for info level logs to be shown.