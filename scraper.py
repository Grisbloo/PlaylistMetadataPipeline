import browser_factory
import storage_manager
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pyautogui
import shutil
import subprocess

# Test playlist: https://open.spotify.com/playlist/0FXuMc11GXo2P3ddHnuTvf

def kill_drivers():
    #Kill all instances of chromedriver and uc_driver.
    try:
        # For Windows
        subprocess.run(["taskkill /f /im chromedriver.exe"], shell=True, capture_output=True)
        subprocess.run(["taskkill /f /im uc_driver.exe"], shell=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        #Don't worry if the drivers cannot be killed assume they will
        pass

def run_pipeline (playlist_link, log_callback):
    #This sends text to the terminal and the GUI
    def system_log(message):
        print(message)
        log_callback(message)
    #Print we are ready to take a users playlist link
    #system_log("System Ready. Waiting for URL...")
    #We don't need the input line that we once had anymore because the gui will give that to the rest of the scraper rather than reading it from the terminal
    #turning on the database
    storage_manager.initialize_database()
    #grab the folder to download to
    local_download_folder = os.path.join(os.getcwd(), "downloads")
    #if the download folder exists dont worry about it, if it doesnt make it
    os.makedirs(local_download_folder, exist_ok=True)
    windows_download_folder = os.path.join(os.path.expanduser("~"), 'Downloads')
    #turning on the browser factory to get me a browser
    driver = browser_factory.BrowserFactory.create_driver(download_folder_path=local_download_folder)
    #if something doesnt work, rather than just crashing, close out of the program
    try:
        #Set up a wait timer in seconds
               #To note: the entire amount of time does not need to pass
        wait = WebDriverWait(driver, 10)
        #travel to the website url
        driver.get("https://www.chosic.com/spotify-playlist-exporter/")
        #find the element we need (search bar) and wait for it to be accessible
        try:
            search_bar = wait.until(EC.element_to_be_clickable((By.ID, "search-word")))
        except Exception as e:
            # The Black Box Recorder
            driver.save_screenshot("crash_report.png")
            system_log("CRITICAL: Element not found. Screenshot saved to crash_report.png")
            raise e
        #click on the search bar
        search_bar.click()
        #input the playlist link into the search bar
        search_bar.send_keys(playlist_link)
        #find the element we need (Start Button) and wait for it to be accessible
        start_button = wait.until(EC.element_to_be_clickable((By.ID, "analyze")))
        #click on the start button
        start_button.click()
         #find the element we need (Export Button) and wait for it to be accessible
        exportCSV = wait.until(EC.presence_of_element_located((By.ID, "export")))
        #click on the export to csv button
        driver.execute_script("arguments[0].click();", exportCSV)
        #This is a dirty hack to bypass the windows explorer download promt since we are in incognito mode
        time.sleep(1) 
        pyautogui.press('enter')

        downloaded_file_path = wait_for_download(windows_download_folder)
    finally:
        driver.quit()
        #Make sure the drivers are gone to prevent unwanted errors
        kill_drivers()
    if downloaded_file_path is None:
        system_log("Download timed out.")
        return
    
    # Now we have the downloaded file, lets move it into the folder
    final_file_path = os.path.join(local_download_folder, os.path.basename(downloaded_file_path))
    shutil.move(downloaded_file_path, final_file_path)
    def duration_to_sectonds(duration_str):
        parts = duration_str.split(":")
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + int(seconds)
        return None
    with open(final_file_path, "r", encoding="utf-8") as file:
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

            is_new_track = storage_manager.log_track(song_id, title, artist, album, year, duration, isrc, downloaded)
            if is_new_track:
                system_log(f"{title} was successfully added to the database.")
            else:
                system_log(f"{title} is a duplicate and was skipped.")

def wait_for_download(download_folder_path):
    i = 0
    while(i < 30):
        #wait for one second
        time.sleep(1)
        files_in_folder = os.listdir(download_folder_path)
        for file in files_in_folder:
            if file.endswith(".csv") and not file.endswith(".crdownload"):
            # The while loop is over once we have our file
                return os.path.join(download_folder_path, file)
        i += 1
            # loop again 
    return None
    #the file was not found in the 30 seconds 

if __name__ == "__main__":
    run_pipeline()
