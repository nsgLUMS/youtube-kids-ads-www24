This folder contains 4 python script. The description for each of these is mentioned below:

1. **query_yt_api.py**: This Python script is designed to fetch information about the most popular videos from a specified YouTube channel using the YouTube API. The collected data is then written into a text file named 'videos.txt'. To execute this script, use the command: python query_yt_api.py

2. **script_final.py**: This serves as the primary Selenium script responsible for extracting advertisement data from a list of videos provided in a text file. The collected ad data is then written into text files. To run this script, execute: python script_final.py <name.txt>, where <name.txt> represents the list of video IDs for which ad data needs to be collected.

3. **script_final_EU.py**: This script is similar to script_final.py but is specifically tailored for countries in Europe. It accounts for an additional terms and conditions button click before playing each video. To use this script, run: python script_final_EU.py <name.txt>

4. **view_counts.py**: This Python script is designed to obtain the view count for each video in a given YouTube channel. To execute this script, use the command: python view_counts.py.
