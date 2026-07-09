import customtkinter as ctk
import threading
import scraper as scraper

# Set the overall theme of the application
ctk.set_appearance_mode("System")  # Follows Windows Dark/Light mode
ctk.set_default_color_theme("blue") 

class SpotifyMetaDataExtractor(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("SpotifyMetaDataExtractor")
        self.geometry("450x600")
        self.resizable(False, False) # Locks window size to prevent layout breaking
    
        # The Title Label
        self.title_label = ctk.CTkLabel(
            self, 
            text="SpotifyMetaDataExtractor", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(30, 10)) # pady adds vertical spacing (top, bottom)

        # The Input Field
        self.url_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Paste Spotify Playlist URL here...",
            width=400,
            height=40
        )
        self.url_entry.pack(pady=20)

        # The Start Button
        self.start_button = ctk.CTkButton(
            self, 
            text="Extract Metadata",
            height=40,
            command=self.start_extraction # This is where we link the button click
        )
        self.start_button.pack(pady=10)
        
        # The Status/Terminal Box
        self.status_box = ctk.CTkTextbox(self, width=400, height=150)
        self.status_box.pack(pady=20)
        self.status_box.insert("0.0", "System Ready. Waiting for URL...\n")
        self.status_box.configure(state="disabled") # Prevents the user from typing in it

        # The Illusion of speed
        self.progress_bar = ctk.CTkProgressBar(self, width=400, mode="indeterminate")  # Indeterminate mode for the bouncing effect
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)  # It is empty at the start

    def write_to_status_box(self, message):
        self.status_box.configure(state="normal")  # Enable editing
        self.status_box.insert("end", message + "\n")  # Append message
        self.status_box.see("end")  # Auto-scroll to the end
        self.status_box.configure(state="disabled")  # Disable editing

    def start_extraction(self):
        url = self.url_entry.get().strip()
        if not url:
            self.write_to_status_box("ERROR: Please enter a valid Spotify URL.")
            return
        if "playlist"not in url.lower():
            self.write_to_status_box("ERROR: The URL does not appear to be a Spotify playlist.")
            return
        self.write_to_status_box("Starting metadata extraction...")
        self.start_button.configure(state="disabled")  # Disable the button to prevent multiple clicks
        self.url_entry.configure(state="disabled")  # Disable the entry to prevent changes during processing
        self.progress_bar.start() #Start the bar bouncing back and forth to give the illusion of speed
        # Run the scraper in a separate thread to prevent blocking the GUI
        thread = threading.Thread(target=self.background_task, args=(url,))
        thread.start()
    
    def background_task(self, url):
        """Run a function in a separate thread and handle GUI updates."""
        try:
            scraper.run_pipeline(url, self.write_to_status_box)
            self.write_to_status_box("Metadata extraction completed successfully.")
        except Exception as e:
            self.write_to_status_box(f"ERROR: {str(e)}")
        finally:
            def restore_gui():
                self.start_button.configure(state="normal")  # Re-enable the button
                self.url_entry.configure(state="normal")  # Re-enable the entry
                self.progress_bar.stop()  # Stop the progress bar
                self.progress_bar.set(0)  # Set the progress bar back to being empty to indicate completion
                self.write_to_status_box("Processing completed.")
            self.after(0, restore_gui)  # Schedule the GUI restoration on the main thread

if __name__ == "__main__":
    app = SpotifyMetaDataExtractor()
    app.mainloop() # This is the infinite loop that keeps the window open