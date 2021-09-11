# vstvgo-homeassistant-dashboard

## description:
The following project was created for watching UStvgo channels via home assistant dashboard, broadcasting to google chromecast. 

Assuming you have a Home Assistant Core (python server) running 
https://www.home-assistant.io/installation/

and you are managing dashboards using YAML files:
https://www.home-assistant.io/lovelace/dashboards/

<img src="https://raw.githubusercontent.com/yishait/ustvgo-homeassistant-dashboard/main/images/demo-light.jpeg" width=250 ><img src="https://raw.githubusercontent.com/yishait/ustvgo-homeassistant-dashboard/main/images/demo-dark.jpeg" width=250 >

### IMPORTANT:
make sure you either DON'T have any settings for:
׳׳׳
lovelace:
  dashboards:
׳׳׳ 

OR you DO have a place-holder
׳׳׳
lovelace:
  dashboards: {}
׳׳׳ 
the script will not work if you ONLY have lovelace: setup like this:
׳׳׳
lovelace:
׳׳׳ 

this project utilizes https://github.com/benmoose39/ustvgo_to_m3u project to get the .m3u streaming files provided by ustvgo.tv, these streams are valid only for ~4 hours and need to be refreshed

when managing the HA dashboards using YAML - no restart is required when refreshing the links in the dashboard.

## Setting up:
go to your ~/.homeassistant folder (where the configuration.yaml is placed)
and run:

```
git clone https://github.com/yishait/ustvgo-homeassistant-dashboard.git
```

once completed, setup the environment by running the setup.sh file
```
source ustvgo-homeassistant-dashboard/scripts/setup.sh
```
A new virtualenv is created, sourced and requirements installed.

add your rooms and the devices used in them to the settings.yaml file:
dashboard_settings:
  room1: 
    devices: 
      - device_1
  room2: 
    devices:
      - device_2

if they dont exist - the script will add them to your configuration.yaml used to run Home-assistant 

## Running channel_dispatcher
once all setup is completed you should see the new alias: channel_dispatcher
and you will be able to run:
```
channel_dispatcher 
```
creating the channel cards and the dashboards according to the setup in settings.yaml, 
you will be prompted the following question:
update stream list? (Y / N)

y = will refetch the m3u links.
n = will only make sure the setup is correct and cards and dashboards are created.

## additional vars:

```
channel_dispatcher --cron true --cron_min X
```
will trigger an exacution every X minutes (when no cron_min is provided the default is 210 min=3.5 hours).

```
channel_dispatcher --log INFO
```
for info level logs to be shown.

## customization

you can customize the board / card templates, change the columns or add additional configuration.
endless possibilities, intro to design here: https://www.juanmtech.com/how-to-set-up-lovelace-on-home-assistant

great information and documentation here: https://www.awesome-ha.com/

more card icons can be found here:
https://cdn.jsdelivr.net/npm/@mdi/font@5.3.45/preview.html