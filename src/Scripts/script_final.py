import time
from unittest import skip
import warnings
import json
import orjson
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from collections import Counter
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import os
import sys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

latencyInMilliseconds = 1
downloadLimitMbps = 13.5
uploadLimitMbps = 100

TIME_TO_SLEEP = float(2 / downloadLimitMbps)

warnings.filterwarnings("ignore", category=DeprecationWarning)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
# chrome_options.add_argument("--headless")
# chrome_options.headless = False
error_list = []
auto_play_toggle = False


def to_seconds(timestr):
    """Convert a time string to seconds.
    timestr: string in the form 'minute:second'
    returns: float number of seconds
    """
    seconds = 0
    for part in timestr.split(":"):
        seconds = seconds * 60 + int(part, 10)
    return seconds

def enable_stats_for_nerds(driver):
    movie = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "movie_player")
            )
    )   
    # video_playing = driver.execute_script(
    #     "return document.getElementById('movie_player').getPlayerState()"
    # )
    # if video_playing == 1:
    #             movie_player.send_keys(Keys.SPACE)
   
    ActionChains(driver).context_click(movie).perform()
    time.sleep(1)
    retry_count = 0
    while retry_count < 5:
        try:
            stats_for_nerds = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[2]/div/div/div[6]")
                )
            )
            stats_for_nerds.click()
            print("Enabled stats collection.")
            return True
        except:
            retry_count += 1

def start_playing_video(driver):
    player_state = driver.execute_script(
        "return document.getElementById('movie_player').getPlayerState()"
    )
    print("Player State: ", player_state)
    if player_state == 5:
        driver.execute_script(
            "document.getElementsByClassName('ytp-large-play-button ytp-button')[0].click()"
        )

    if player_state == 1:
        return

def play_video_if_not_playing(driver):

    player_state = driver.execute_script(
        "return document.getElementById('movie_player').getPlayerState()"
    )
    if player_state == 0:
        return

    if player_state == -1:
        driver.execute_script(
            "document.getElementsByClassName('video-stream html5-main-video')[0].play()"
        )
        
    if player_state != 1:
        driver.execute_script(
            "document.getElementsByClassName('video-stream html5-main-video')[0].play()"
        )

def get_ad_info(driver, movie_id):
    # print("Inside Video info", movie_id)

    ad_id = driver.execute_script(
        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
    )
    time.sleep(0.3)
    skippable_add = driver.execute_script(
        'return document.getElementsByClassName("ytp-ad-skip-button-container").length'
    )
    print("Add is skippable? ",skippable_add)
    if skippable_add:
        try:
            skip_duration = int(
                driver.execute_script(
                    'return document.getElementsByClassName("ytp-ad-text ytp-ad-preview-text")[0].innerText'
                )
            )
        except:
            skip_duration = -2  # Error occured, Could not get Skip Duration
    else:
        skip_duration = 999  # Add was not skippable.


    time.sleep(0.5)
    while str(ad_id) == str(movie_id):
        ad_id = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
        )

    # print("Ad Id is" + str(ad_id))
    return ad_id, skippable_add, skip_duration

def driver_code(driver, filename):
    with open(filename, "r") as f:
        list_of_urls = f.read().splitlines()
    # list_of_urls = ['IC25DUOSIpw', 'Kn_4thbpArM', 'S0NlS1vwm-c', 'pK1n2HGkrug', '6ZKa8DR-gbU', 'VNUjQy60bDQ', 'F2VL0hacY74', 'AWmSZOwQb80', 'UCvTs7mUo84', '1B2foBjNkf8']
    filename = str(filename)
    folder_name = filename.split('.')
    new_dir = "./" + str(folder_name[0])
    
    for index, url in enumerate(list_of_urls):
        # url = "https://www.youtube.com/watch?v=" + str(url)
        global error_list
        global auto_play_toggle
        video_info_details = {}
        error_list = []
        unique_add_count = 0

        previous_ad_id = url.split("=")[1]
        movie_id = url.split("=")[1]
        time.sleep(2)
        driver.get(url)
        movie_player = driver.find_element_by_id('movie_player')
        video_playing = driver.execute_script(
                "return document.getElementById('movie_player').getPlayerState()"
            )
        if video_playing == 1:
                movie_player.send_keys(Keys.SPACE)
        try:
            # Enable Stats
            enable_stats_for_nerds(driver)

            # Start Playing Video
            start_playing_video(driver)


            # Check If ad played at start
            # time.sleep(TIME_TO_SLEEP)
            ad_playing = driver.execute_script(
                "return document.getElementsByClassName('ad-showing').length"
            )

            if ad_playing:
                ad_id, skippable, skip_duration = get_ad_info(driver, movie_id)
                if ad_id not in video_info_details.keys():
                    if ad_id != "empty_video ":
                        unique_add_count += 1
                        video_info_details[ad_id] = {
                            "Count": 1,
                            "Skippable": skippable,
                            "SkipDuration": skip_duration,
                        }
                        previous_ad_id = ad_id
                        print("Advertisement " + str(unique_add_count) + " Data collected.")

            print("Playing Video",index, ":", movie_id)

            video_duration_in_seconds = driver.execute_script(
                'return document.getElementById("movie_player").getDuration()'
            )

            Path(new_dir).mkdir(parents=False, exist_ok=True)

            video_playing = driver.execute_script(
                "return document.getElementById('movie_player').getPlayerState()"
            )
            
            if video_playing != 1:
                print("Video has now started playing")
                movie_player.send_keys(Keys.SPACE)
            else:
                print("Video is already playing")

            ad_playing = driver.execute_script(
                "return document.getElementsByClassName('ad-showing').length"
            )

            if ad_playing:
                ad_id, skippable, skip_duration = get_ad_info(driver, movie_id)
                if ad_id not in video_info_details.keys():
                    if ad_id != "empty_video ":
                        unique_add_count += 1
                        video_info_details[ad_id] = {
                            "Count": 1,
                            "Skippable": skippable,
                            "SkipDuration": skip_duration,
                        }
                        previous_ad_id = ad_id
                        print("Advertisement " + str(unique_add_count) + " Data collected.")

            # Turning off Autoplay
            if not auto_play_toggle:
                try:
                    driver.execute_script(
                        "document.getElementsByClassName('ytp-autonav-toggle-button-container')[0].click()"
                    )
                    auto_play_toggle = True
                except:
                    pass

            while True:
                # time.sleep(0.5)
                play_video_if_not_playing(driver)
                video_playing = driver.execute_script(
                    "return document.getElementById('movie_player').getPlayerState()"
                )

                # time.sleep(0.5)
                ad_playing = driver.execute_script(
                    "return document.getElementsByClassName('ad-showing').length"
                )
                # time.sleep(0.5)

                b_ad=[]
                b_ad = driver.find_elements(By.ID,'action-companion-click-target')
                if (b_ad and b_ad != []):
                    try: 
                        banner_ad_img = driver.execute_script(
                            "return document.getElementById('action-companion-click-target').childNodes[1].children[0].src"
                        )

                        banner_ad_text = driver.execute_script(
                            "return document.getElementById('action-companion-click-target').childNodes[3].children['text'].children['header'].innerText"
                        )

                        banner_ad_url = driver.execute_script(
                            "return document.getElementsByClassName('style-scope ytd-action-companion-ad-renderer')[10].innerHTML"
                        )
                        if ((banner_ad_num>1 and prev_banner_ad!=banner_ad_url) or banner_ad_num==1):
                            video_info_details["Banner Ad" + str(banner_ad_num)] = {
                            "ImgSrc": banner_ad_img,
                            "Url": banner_ad_url,
                            "Text": banner_ad_text
                            }
                            banner_ad_num = banner_ad_num + 1
                    
                        prev_banner_ad=banner_ad_url
                    except:
                        pass

                sidebar = []
                sidebar = driver.find_elements(By.CLASS_NAME,'style-scope ytd-promoted-sparkles-web-renderer')
                if (sidebar and sidebar != [] and len(sidebar) > 0):
                    try: 
                        sidebar_img = driver.execute_script(
                            "return document.getElementsByClassName('style-scope ytd-promoted-sparkles-web-renderer')[4].children[0].src"
                        )

                        sidebar_title = driver.execute_script(
                            "return document.getElementsByClassName('style-scope ytd-promoted-sparkles-web-renderer')[9].title"
                        )

                        sidebar_desc = driver.execute_script(
                            "return document.getElementsByClassName('style-scope ytd-promoted-sparkles-web-renderer')[10].innerText"
                        )

                        sidebar_link = driver.execute_script(
                            "return document.getElementsByClassName('style-scope ytd-promoted-sparkles-web-renderer')[11].childNodes[3].innerText"
                        )
                    
                        if ("Sidebar" not in video_info_details.keys()):
                            video_info_details["Sidebar"] = {
                            "Img": sidebar_img,
                            "Title": sidebar_title,
                            "Description":sidebar_desc,
                            "Link":sidebar_link
                            }
                    except:
                        pass

                infeed = []
                infeed = driver.find_elements(By.CLASS_NAME,'style-scope ytd-in-feed-ad-layout-renderer')
                if (infeed and infeed != [] and len(infeed) > 0):
                    try: 
                        infeed_img = driver.execute_script(
                            "return document.getElementsByClassName('style-scope ytd-in-feed-ad-layout-renderer')[0].firstChild.children[0].children['thumbnail'].children[0].children[0].src"
                        )

                        infeed_title = driver.execute_script(
                            "return document.getElementsByClassName('style-scope ytd-in-feed-ad-layout-renderer')[0].firstChild.children[1].children['endpoint-link'].children[0].innerText"
                        )

                        infeed_channel = driver.execute_script(
                            "return document.getElementsByClassName('style-scope ytd-in-feed-ad-layout-renderer')[0].firstChild.children[1].children['endpoint-link'].children[1].children[0].children['metadata'].children['byline-container'].children['channel-name'].innerText"
                        )

                        infeed_link = driver.execute_script(
                            "return document.getElementsByClassName('style-scope ytd-in-feed-ad-layout-renderer')[0].firstChild.children[0].children['thumbnail'].href"
                        )
                    
                        if ("In-feed" not in video_info_details.keys()):
                            video_info_details["In-feed"] = {
                            "Img": infeed_img,
                            "Title": infeed_title,
                            "Channel":infeed_channel,
                            "Link":infeed_link
                            }
                    except:
                        pass

                ad_playing = driver.execute_script(
                    "return document.getElementsByClassName('ad-showing').length"
                )
                # time.sleep(0.5)

                video_playing = driver.execute_script(
                    "return document.getElementById('movie_player').getPlayerState()"
                )

                if ad_playing:
                    # Ad is being played
                    print("Ad Playing")

                    ad_id, skippable, skip_duration = get_ad_info(
                        driver, movie_id
                    )
                    if (str(ad_id).strip()) != (str(movie_id).strip()):
                        if ad_id != previous_ad_id:
                            if ad_id != "empty_video ":
                                print("Ad id is: ", ad_id)
                                previous_ad_id = ad_id

                            if ad_id not in video_info_details.keys():
                                if ad_id != "empty_video ":
                                    unique_add_count += 1
                                    video_info_details[ad_id] = {
                                        "Count": 1,
                                        "Skippable": skippable,
                                        "SkipDuration": skip_duration,
                                    }
                                    print(
                                        "Advertisement "
                                        + str(unique_add_count)
                                        + " Data collected."
                                    )
                            else:
                                current_value = video_info_details[ad_id]["Count"]
                                video_info_details[ad_id]["Count"] = current_value + 1
                                print("Count of existing add increased!")


                elif video_playing == 0:
                    # Video has ended
                    file_dir = new_dir + "/" + str(movie_id) + ".txt"
                    video_info_details["Main_Video"] = {
                        "Url": url,
                        "Total Duration": video_duration_in_seconds,
                        "UniqueAds": unique_add_count,
                    }
                    with open(file_dir, "wb+") as f:
                        f.write(orjson.dumps(video_info_details))
                    video_info_details = {}
                    unique_add_count = 0
                    print("Video Finished and details written to files!")
                    break
                else:
                    # Video is playing normally
                    previous_ad_id = url.split("=")[1]
        except Exception as e:
            print(e)
            print("Error occured while collecting data! Moving to next video!")
            print("Video: ", url)
            with open("faultyVideos.txt", "a") as f:
                to_write = str(url) + "\n"
                f.write(to_write)
            continue



driver = webdriver.Chrome(options=chrome_options)

filename = sys.argv[1]
driver_code(driver, filename)
driver.quit()

