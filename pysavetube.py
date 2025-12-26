from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import subprocess
import pyfiglet
import os
from termcolor import colored
import sys
import ffmpeg


#Clear terminal, setup text
subprocess.run("clear")
f = pyfiglet.figlet_format("PySaveTube")
print(colored(f, "yellow"))
print("\nA simple wrapper for the pytubefix library, utilising FFMpeg and bash.\n")

#User inputs URL and format to save as; while loop for invalid URLs, recognition for playlists
while True:
    url = input("Enter URL: ")
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        isplaylist = False
    except Exception:
        try:
            pl = Playlist(url)
            isplaylist = True
            break
        except Exception:
            print("Invalid URL.")
    else:
        break
format = input("Format to save video(s) as (must be ffmpeg supported): ")

if isplaylist == False:

    print(f"Downloading {yt.title}...")


    yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True).order_by("resolution").desc().first().download(filename="video.mp4")
    yt.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by("abr").desc().first().download(filename="audio.mp4")

    #Recombine with ffmpeg
    subprocess.run(["ffmpeg", "-i", "video.mp4", "-i", "audio.mp4", "-c", "copy", f"{yt.title}.mp4"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    #Move file to downloads
    subprocess.run(["mv", f"{yt.title}.mp4", f"{os.path.expanduser("~")}/Downloads/"])

    #Change file to desired format
    subprocess.run(["ffmpeg", "-i", f"{os.path.expanduser("~")}/Downloads/{yt.title}.mp4", f"{os.path.expanduser("~")}/Downloads/{yt.title}.{format}"])

    #Remove original audio and video files
    subprocess.run(["rm", "audio.mp4", "video.mp4", f"{os.path.expanduser("~")}/Downloads/{yt.title}.mp4"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

else:

    print(f"Downloading {pl.title}...")

    subprocess.run(["mkdir", f"{pl.title}"])

    for video in pl.videos:

        video.streams.filter(adaptive=True, file_extension="mp4", only_video=True).order_by("resolution").desc().first().download(filename="video.mp4")
        video.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by("abr").desc().first().download(filename="audio.mp4")

        subprocess.run(["ffmpeg", "-i", "video.mp4", "-i", "audio.mp4", "-c", "copy", f"{video.title}.mp4"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        subprocess.run(["ffmpeg", "-i", f"{video.title}.mp4", f"{video.title}.{format}"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        subprocess.run(["rm", "audio.mp4", "video.mp4", f"{video.title}.mp4"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        subprocess.run(["mv", f"{video.title}.{format}", f"{pl.title}/"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    subprocess.run(["mv", f"{pl.title}/", f"{os.path.expanduser("~")}/Downloads/Run 3/"])

print("Downloaded! Please check your downloads folder.")
