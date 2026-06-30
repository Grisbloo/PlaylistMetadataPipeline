import browser_factory
import storage_manager
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Test playlist: https://open.spotify.com/playlist/0FXuMc11GXo2P3ddHnuTvf

def main ():
    #input allows command line input
    playlist_link = input("Spotify playlist or song URL: ")
    #turning on the database
    storage_manager.initialize_database()
    #if the download folder exists dont worry about it, if it doesnt make it
    os.makedirs(download_folder_path, exist_ok=True)
    #grab the folder to download to
    download_folder_path = os.path.join(os.getcwd(), "downloads")
    #turning on the browser factory to get me a browser
    driver = browser_factory.BrowserFactory.create_driver(download_folder_path=download_folder_path)
    #if something doesnt work, rather than just crashing, close out of the program
    try:
        #Set up a wait timer in seconds
               #To note: the entire amount of time does not need to pass
        wait = WebDriverWait(driver, 10)
        #travel to the website url
        driver.get("https://www.chosic.com/spotify-playlist-exporter/")
        #find the element we need (search bar) and wait for it to be accessible
        search_bar = wait.until(EC.element_to_be_clickable((By.ID, "search-word")))
        #click on the search bar
        search_bar.click()
        #input the playlist link into the search bar
        search_bar.send_keys(playlist_link)
        #find the element we need (Start Button) and wait for it to be accessible
        start_button = wait.until(EC.element_to_be_clickable((By.ID, "analyze")))
        #click on the start button
        start_button.click()
         #find the element we need (Export Button) and wait for it to be accessible
        exportCSV = wait.until(EC.element_to_be_clickable((By.ID, "export")))
        #click on the export to csv button
        exportCSV.click()
    finally:
        downloaded_file = wait_for_download(download_folder_path)
        driver.quit()
    if downloaded_file is None:
        print("Download timed out.")
        return
    file_path = os.path.join(download_folder_path,downloaded_file)
    def duration_to_sectonds(duration_str):
        parts = duration_str.split(":")
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + int(seconds)
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:

            song_id = row["Spotify Track Id"]
            title = row["Song"]
            artist = row["Artist"]
            album = row["Album"]
            year_raw = row["Album Date"][:4] if row["Album Date"] else None
            year = int(year_raw) if year_raw and year_raw.isdigit() else None
            duration = duration_to_sectonds(row["Duration"])
            isrc = row["ISRC"]
            downloaded = False
            storage_manager.log_track(song_id, title, artist, album, year, duration, isrc, downloaded)
def wait_for_download(download_folder_path):
    i = 0
    while(i < 30):
        #wait for one second
        time.sleep(1)
        files_in_folder = os.listdir(download_folder_path)
        for file in files_in_folder:
            if file.endswith(".csv") and not file.endswith(".crdownload"):
            # The while loop is over once we have our file
                return file
        i += 1
            # loop again 
    return None
    #the file was not found in the 30 seconds 
