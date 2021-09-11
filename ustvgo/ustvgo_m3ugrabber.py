import os
import sys
import pathlib 
import logging
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout, 
                    filemode = "w",
                    format = Log_Format, 
                    # level = logging.sys.argv[2])
                    level = "INFO")

logger = logging.getLogger()
banner = r'''
                    #########################################################################
                    #      ____            _           _   __  __                           #
                    #     |  _ \ _ __ ___ (_) ___  ___| |_|  \/  | ___   ___  ___  ___      #
                    #     | |_) | '__/ _ \| |/ _ \/ __| __| |\/| |/ _ \ / _ \/ __|/ _ \     #
                    #     |  __/| | | (_) | |  __/ (__| |_| |  | | (_) | (_) \__ \  __/     #
                    #     |_|   |_|  \___// |\___|\___|\__|_|  |_|\___/ \___/|___/\___|     #
                    #                   |__/                                                #
                    #                                  >> https://github.com/benmoose39     #
                    #########################################################################
'''
logger.info(banner)

windows = False
python = 'python3'
if 'win' in sys.platform:
    windows = True
    python = 'python'

def done():
    logger.info("channels refreshed.")
    # sys.exit()
    
logger.info('[*] Checking dependencies...')
while True:
    try:
        import requests
        from tqdm import tqdm
        break
    except ModuleNotFoundError as e:
        module = str(e)[17:-1]
        logger.info(f'[*] Installing {module} module for python')
        #os.system(f'{python} -m pip install --upgrade pip')
        try:
            if os.system(f'{python} -m pip install {module}') != 0:
                raise error
        except Exception:
            logger.info(f'[!] Error installing "{module}" module. Do you have pip installed?')
            input(f'[!] Playlist generation failed. Press Ctrl+C to exit...')
            done()

def grab(name, code, logo):
    data = {'stream': code}
    m3u = s.post('https://ustvgo.tv/data.php', data=data).text
    playlist.write(f'\n#EXTINF:-1 tvg-id="{code}" group-title="ustvgo" tvg-logo="{logo}", {name}')
    playlist.write(f'\n{m3u}')

total = 0
main_path = pathlib.Path(__file__).parent.resolve()
os.chdir(main_path)
with open("ustvgo_channel_info.txt") as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        total += 1

s = requests.Session()
with open('ustvgo_channel_info.txt') as file:
    with open('ustvgo.m3u', 'w') as playlist:
        logger.info('[*] Generating your playlist, please wait...\n')
        playlist.write('#EXTM3U x-tvg-url="https://raw.githubusercontent.com/Theitfixer85/myepg/master/blueepg.xml.gz"')
        playlist.write(f'\n{banner}\n')
        pbar = tqdm(total=total)
        for line in file:
            line = line.strip()
            if not line or line.startswith('~~'):
                continue
            line = line.split('|')
            name = line[0].strip()
            code = line[1].strip()
            logo = line[2].strip()
            pbar.update(1)
            grab(name, code, logo)
        pbar.close()
        logger.info('\n[SUCCESS] Playlist is generated!\n')
        done()
        
