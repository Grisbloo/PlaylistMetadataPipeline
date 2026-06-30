from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BrowserFactory:
    #This prevents python from making the function about itself and makes it a tool to be used
    @staticmethod
    def create_driver(is_headless=True, download_folder_path =None):
        chrome_options = Options()
        if is_headless:
            #This prevents a ui from appearing when using the browser
            chrome_options.add_argument("--headless")
            #This prevents the gpu from makign the webpage draw faster when using the browser
            chrome_options.add_argument("--disable-gpu")
            #Allow chrome to run normally when using the browser
            chrome_options.add_argument("--no-sandbox")
        if download_folder_path:
            chrome_options.add_experimental_option("prefs", {
                "download.default_directory": download_folder_path,
                "download.prompt_for_download": False,
        })
        driver = webdriver.Chrome(options = chrome_options)
        return driver