import requests
import json 
import os
import yt_dlp
from dotenv import load_dotenv
import base64
from googleapiclient.discovery import build
import customtkinter
from tkinter import Message,messagebox

def convert(playlist):
    
    if playlist == "":
        messagebox.showerror("Please enter a playlist url.")
        return False

    new = customtkinter.CTkToplevel()
    new.geometry("300x300")

    load_dotenv()

    cliend_id = os.getenv("CLIENT_ID")
    cliend_secret = os.getenv("CLIENT_SECRET")

    playlist_id = playlist.split('/')[-1].split('?')[0]

    def get_auth():
        auth_string = cliend_id + ":" + cliend_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization" : "Basic " + auth_64,
            "content-type" : "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}
        result = requests.post(url = url,data  = data,headers  = headers)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token


    def get_auth_token(token):
        return {"Authorization" : "Bearer " + token}

    token = get_auth()

    spotify_playlist_url = "https://api.spotify.com/v1/playlists/" + playlist_id

    try:
        response = requests.get(url = spotify_playlist_url, headers= get_auth_token(token))
        json_result = json.loads(response.content)['tracks']

        tracks_dt = json_result["items"]
    except:
        messagebox.showerror("Invalid Playlist")
        return False

    tracks = []

    for i in range(len(tracks_dt)):
        track_name = tracks_dt[i]["track"]["name"] + " by " + tracks_dt[i]["track"]["artists"][0]["name"]
        tracks.append(track_name)



    url = "https://www.youtube.com/watch?v="
    API_KEY = os.getenv("API_KEY")

    youtube = build('youtube','v3',developerKey= API_KEY)

    def download(Vurl):
        video_info = yt_dlp.YoutubeDL().extract_info(url = Vurl,download=False)
        filename = f"{video_info['title']}.mp3"
        options={
                'format':'bestaudio/best',
                'outtmpl':filename,
            }
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        print("Download complete... {}".format(filename))

    for j,i in enumerate(tracks):
        request = youtube.search().list(
        part = 'snippet',
        q = i,
        type = 'video'
        )
        res = request.execute()
        act_url = url+res['items'][0]['id']['videoId']

        label = customtkinter.CTkLabel(new, text = f"Downloading {i}")
        label.grid(row = j,column = 0)
        download(act_url)

    

        
