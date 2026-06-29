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
    #turning on the browser factory to get me a browser
    driver = browser_factory.BrowserFactory.create_driver()
    #if something doesnt work, rather than just crashing, close out of the program
    try:
        #travel to the website url
        driver.get("https://www.chosic.com/spotify-playlist-exporter/")
        #find the element we need
        search_bar = driver.find_element(By.ID, "search-word")
        #do something with that element
        search_bar.send_keys(playlist_link)
        start_button = driver.find_element(By.ID, "analyze")
        start_button.click()
        #set up a wait timer in seconds
        wait = WebDriverWait(driver, 10)
        #use the stopwatch to count down until the button is avaliable
        #To note: the entire amount of time does not need to pass
        exportCSV = wait.until(EC.element_to_be_clickable((By.ID, "export")))
        exportCSV.click()
    finally:
        driver.quit()

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
