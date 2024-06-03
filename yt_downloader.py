import customtkinter as ctk
from tkinter import filedialog, messagebox
from pytube import YouTube
import re

# Global variable for folder name
Folder_Name = ""


# Function to open file dialog to select the save location
def open_location():
    global Folder_Name
    Folder_Name = filedialog.askdirectory()
    if len(Folder_Name) > 0:
        locationError.configure(text=Folder_Name, text_color="green")
    else:
        locationError.configure(text="Please Choose Folder!!", text_color="red")


# Progress function to update progress bar and label
def progress_function(stream, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar.set(percentage_of_completion / 100)
    progress_label.configure(text=f"Downloaded: {int(percentage_of_completion)}%")
    root.update_idletasks()


# Function to validate YouTube URL
def validate_url(url):
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$'
    return re.match(youtube_regex, url)


# Function to download video
def download_video():
    url = ytdEntryVar.get()
    if len(url) > 1:
        if validate_url(url):
            ytdError.configure(text="")
            try:
                yt = YouTube(url, on_progress_callback=progress_function)
                choice = ytdchoices.get()
                if choice == "Highest Quality":
                    select = yt.streams.get_highest_resolution()
                elif choice == "720p":
                    select = yt.streams.filter(progressive=True, res="720p").first()
                elif choice == "144p":
                    select = yt.streams.filter(progressive=True, res="144p").first()
                elif choice == "Only Audio":
                    select = yt.streams.filter(only_audio=True).first()
                else:
                    ytdError.configure(text="Select a quality option!", text_color="red")
                    return

                if select:
                    messagebox.showinfo("Message", "Your download has started!")
                    select.download(Folder_Name)
                    messagebox.showinfo("Message", "Download Completed!")
                    ytdError.configure(text="Download Completed!!", text_color="green")
                else:
                    ytdError.configure(text="Stream not found!", text_color="red")

            except Exception as e:
                ytdError.configure(text="Failed to download video!", text_color="red")
                messagebox.showerror("Error", f"Error: {e}")
        else:
            ytdError.configure(text="Please enter a valid YouTube URL!", text_color="red")
    else:
        ytdError.configure(text="Please enter a valid URL!", text_color="red")


# Set the appearance and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main window
root = ctk.CTk()
root.title("YouTube Downloader")
root.geometry("500x550")
root.grid_columnconfigure(0, weight=1)

# Ytd Link Label
ytdLabel = ctk.CTkLabel(root, text="Enter the URL of the Video", font=("Arial", 15))
ytdLabel.grid(pady=15)

# Entry Box
ytdEntryVar = ctk.StringVar()
ytdEntry = ctk.CTkEntry(root, width=400, textvariable=ytdEntryVar)
ytdEntry.grid(pady=5)

# Error Msg
ytdError = ctk.CTkLabel(root, text="", text_color="red", font=("Arial", 10))
ytdError.grid()

# Asking save file label
saveLabel = ctk.CTkLabel(root, text="Save the Video File", font=("Arial", 15, "bold"))
saveLabel.grid(pady=10)

# btn of save file
saveEntry = ctk.CTkButton(root, width=150, text="Choose Path", command=open_location)
saveEntry.grid(pady=5)

# Location Error Msg
locationError = ctk.CTkLabel(root, text="", text_color="red", font=("Arial", 10))
locationError.grid()

# Download Quality
ytdQuality = ctk.CTkLabel(root, text="Select Quality", font=("Arial", 15))
ytdQuality.grid(pady=10)

# combobox
choices = ["Highest Quality", "720p", "144p", "Only Audio"]
ytdchoices = ctk.CTkComboBox(root, values=choices, width=150)
ytdchoices.grid(pady=5)

# download btn
downloadbtn = ctk.CTkButton(root, text="Download", width=150, command=download_video)
downloadbtn.grid(pady=20)

# Progress bar
progress_label = ctk.CTkLabel(root, text="Progress: 0%", font=("Arial", 12))
progress_label.grid(pady=10)
progress_bar = ctk.CTkProgressBar(root, width=400)
progress_bar.grid(pady=5)
progress_bar.set(0)

# developer Label
developerlabel = ctk.CTkLabel(root, text="Made by Sumer Sarwan 😁😁", font=("Arial", 15))
developerlabel.grid(pady=10)

# Run the main loop
root.mainloop()
