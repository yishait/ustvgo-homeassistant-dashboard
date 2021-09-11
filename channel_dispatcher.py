#!/usr/bin/env python3
import re
from jinja2 import Template
import os
from pathlib import Path
import sys
import pathlib
import logging
import argparse
import schedule
from ruamel.yaml import YAML
from yamlinclude import YamlIncludeConstructor
main_path = pathlib.Path(__file__).parent.resolve()

parser = argparse.ArgumentParser(description="Creating dashboards and links to streams from ustvgo")
parser.add_argument("--cron",type=str,choices=['true', 'false'], default="false", )
parser.add_argument("--cron_min",type=int, default="210",help="the number of minutes between execution")
parser.add_argument("--log",type=str,choices=['INFO', 'ERROR'], default="ERROR", help="Set the log level")
args = parser.parse_args()

yaml=YAML()
yaml.default_flow_style = False
yaml=YAML(typ='rt')
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True

settings_path = str(main_path)+"/settings.yaml"
dashboard_path = "../dashboards"
dashboard_configuration_path = str(main_path)+"/../configuration.yaml"
ustvgo_path = str(main_path)+"/ustvgo"
templates_path = str(main_path)+"/templates"

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout, 
                    filemode = "w",
                    format = Log_Format, 
                    level = args.log)

logger = logging.getLogger()


def validate_dashboards_folder():
    os.chdir(main_path)
    Path("../dashboards").mkdir(parents=True, exist_ok=True)

def load_configuration(dashboard_configuration_path):
    dashboard_configuration = yaml.load(open(dashboard_configuration_path))
    return dashboard_configuration

def configured_boards(dashboard_configuration_path):
    boards = []
    configuration = load_configuration(dashboard_configuration_path)
    try:
        configured_boards = configuration["lovelace"]['dashboards']
        for room in configured_boards:
            boards.append(room.split("lovelace-",1)[1])
        return boards
    except:
        return [""]


def load_settings(settings_path):
    f = open(settings_path, "r")
    settings_file = f.read()
    settings = yaml.load(settings_file)["dashboard_settings"]
    return settings

# Running ustvgo_to_m3u to get the latest streaming links
def fetching_channels():
    channels_res = {}
    f = open(ustvgo_path+"/ustvgo.m3u", "r")
    for line in f:
        if "https://h" in line:
            url = line
            url = url.rstrip('\n')
            ch = re.search(r'ustvgo.la\/(.*?)\/myStream', line).group(1)
            channels_res[ch] = url
    return channels_res

# Create cards using templates and values
def create_cards(channels, device):
    cards = ""
    f = open("templates/card_template", "r")
    card_temp = f.read()
    tm = Template(card_temp)
    for channel in channels:
        msg = tm.render(url=channels[channel], channel=channel, player=device)
        if len(cards) > 0:
            cards = cards + "\n" + msg
        else:
            cards = msg
    return cards

# create dashboard using template and values
def create_dashboard_conf(board):
    os.chdir(main_path)
    f = open("templates/board_conf_template", "r")
    tm = Template(f.read())
    board_conf = tm.render(board=board)
    return board_conf

def update_yaml_configuration_changes(conf_changed, yaml_path):
    with open(yaml_path, 'w') as fp:
        yaml.dump(conf_changed,fp)

def update_board_conf(conf,dashboard_configuration_path):
    configuration = load_configuration(dashboard_configuration_path)
    conf_dict=yaml.load(conf)

    if 'lovelace' not in configuration:
        love = yaml.load(lovelace_block())
        configuration.update(love)
    configuration['lovelace']['dashboards'].update(conf_dict)
    update_yaml_configuration_changes(configuration,dashboard_configuration_path)

def create_dashboard(cards, selected_device, selected_board_key):
    f = open("templates/board_template", "r")
    board_temp = f.read()
    tm = Template(board_temp)
    board = tm.render(board_key=selected_board_key,
                      board_cards=cards, device=selected_device)
    return board

def lovelace_block():
    f = open(templates_path+"/lovelace_block_template", "r")
    love = f.read()
    return love

def save_latest(dashboard, selected_board_key):
    os.chdir(dashboard_path)
    f = open(selected_board_key+".yaml", "w")
    f.write(dashboard)
    f.close()

def execute_update():
    # Refresh the ustvgo.m3u file, by default if run by cron
    if args.cron == "true":
        update = "y"
    else:
        print("update stream list? (Y / N)")
        update = input()
    if "Y" == update or "y" == update:
        from ustvgo import ustvgo_m3ugrabber

    rooms = load_settings(settings_path)
    existing_boards = configured_boards(dashboard_configuration_path)
    new_dashboard_configuration = ""
    channels = fetching_channels()
    logger.info("channels fetched.")

    for room in rooms:
        if room not in existing_boards:
            validate_dashboards_folder()
            logger.info("Room:"+room+" Not in existing boards adding.")
            room_conf=create_dashboard_conf(room)
            new_dashboard_configuration = new_dashboard_configuration + room_conf + "\n"
    
        for device in rooms[room]['devices']:
            os.chdir(main_path)
            selected_device = device
            selected_board_key = room

            cards = create_cards(channels, selected_device)
            logger.info("cards created.")

            dashboard = create_dashboard(cards, selected_device, selected_board_key)
            save_latest(dashboard, selected_board_key)
            logger.info(selected_board_key+" dashboard saved.")

    if len(new_dashboard_configuration) > 0:
        logger.info("Adding the following to configuration.yaml file.\n"+new_dashboard_configuration)
        update_board_conf(new_dashboard_configuration, dashboard_configuration_path)
    print("Done.")

try:
    if args.cron == "false":
        execute_update()
    else:
        logger.info("starting in schedule mode, next run in: "+ str(args.cron_min) + " minutes")
        schedule.every(args.cron_min).minutes.do(execute_update) 
        while True:
            schedule.run_pending()
except:
    print("Operation stopped.")