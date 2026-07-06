from seleniumbase import Driver

class BrowserFactory:
    @staticmethod
    def create_driver(is_headless=True, download_folder_path=None):
        # Driver automatically handles the anti-detect masking (uc=True)
        # headless2 is the stealth headless mode (avoids instant WAF bans)
        driver = Driver(
            uc=True,
            incognito=True, 
            headless2=is_headless, 
            window_size="1920,1080"
        )
        
        # Safely route downloads without triggering automation flags
        if download_folder_path:
            driver.execute_cdp_cmd(
                "Browser.setDownloadBehavior",
                {
                    "behavior": "allow",
                    "downloadPath": download_folder_path,
                    "eventsEnabled": True
                }
            )
            
        return driver