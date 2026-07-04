from selenium import webdriver
from selenium.webdriver.edge.options import Options

class BrowserFactory:
    #This prevents python from making the function about itself and makes it a tool to be used
    @staticmethod
    def create_driver(is_headless=True, download_folder_path =None):
        edge_options = Options()
        #This prevents a ui from appearing when using the browser
        edge_options.add_argument("--headless")
        #Forces the browser to create a specific window size where all buttons are visible
        edge_options.add_argument("--window-size=1920,1080")
        #Removal of the automation flags and banners
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option("useAutomationExtension", False)
        #This prevents the gpu from makign the webpage draw faster when using the browser
        edge_options.add_argument("--disable-gpu")
        #Allow edge to run normally when using the browser
        edge_options.add_argument("--no-sandbox")
        prefs = {
            "download.default_directory": download_folder_path,
            "download.prompt_for_download": False,
        }
        edge_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Edge(options=edge_options)
        #Removal of the Webdriver fingerprint that Cloudflare uses to detect automation
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})
        return driver