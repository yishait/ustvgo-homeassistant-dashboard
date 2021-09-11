# vstvgo-homeassistant-dashboard

The following repo was created for watching UStvgo channels via home assistant dashboard, broadcasting to google chromecast. 

Assuming you have a Home Assistant Core (python server) running 
https://www.home-assistant.io/installation/

and you are managing dashboards using YAML files (not the UI)

this project utilizes https://github.com/benmoose39/ustvgo_to_m3u project to get the .m3u streaming files provided by ustvgo.tv, these streams are valid only for ~4 hours and need to be refreshed,
when managing the HA dashboards using YAML - no restart is required when refreshing the links.


add this to configuration.yaml
lovelace: 
  dashboards:
    lovelace-salon: 
      mode: yaml
      filename: dashboards/salon.yaml
      title: salon