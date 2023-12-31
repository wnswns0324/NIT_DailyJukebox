import instagrapi
import time
import datetime
import os

from moviepy.editor import *
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import AudioFileClip

from PIL import Image, ImageDraw, ImageFont

from envManager import *


genre = ["Jazz", "POP", "EDM"]

def login_instagram(username, password):
    print("Logging In...")
    api = instagrapi.Client(request_timeout=5)
    api.login(username, password)
    return api

def post_instagram(api, image_path, track_name, artist_name, album_name, preview, index):
    now = datetime.datetime.now()
    upload_data = []
    upload_msg = []
    print("Post Activated")
    
    create_thumbnail()
    upload_data.append("today.jpg")
    upload_msg.append(f"{datetime.datetime.now().strftime('%m.%d')} Recommendation of Today")

    for i in range(3):
        if preview[i][index] == None:
            print(f"{ artist_name[i][index] } - { track_name[i][index] }, Image adding")
            upload_data.append( image_path[i][index] )
            upload_msg.append(f"\n\nToday's { genre[i] }\n{ artist_name[i][index] } - { track_name[i][index] }\nfrom the album { album_name[i][index] }")
            print("Image added\n")   
            print(upload_data)
            print(upload_msg)
        else:
            print(f"{ artist_name[i][index] } - { track_name[i][index] }, Video Producing")
            create_preview_video(image_path[i][index], preview[i][index])
            print(f"Video Produced for { artist_name[i][index] } - { track_name[i][index] }")

            upload_data.append(os.path.join("preview_video", f"{genre[i]}_{index}.mp4"))
            upload_msg.append(f"\n\nToday's { genre[i] }\n{ artist_name[i][index] } - { track_name[i][index] }\nfrom the album { album_name[i][index] }")
            print(f"Video added\n")
            print(upload_data)
            print(upload_msg)

    api.album_upload(paths=upload_data, caption='\n'.join(upload_msg))
    print("Upload Completed")
    time.sleep(5)



def create_preview_video(image_path, preview):
    music_preview = AudioFileClip(preview)
    video_length = 30
    
    album_image = ImageClip(image_path)
    album_image.fps = 24
    
    video = album_image.set_duration(video_length).set_audio(music_preview)
    
    output_directory = os.path.join("preview_video", f"{os.path.basename(image_path[:-4])}.mp4")
    video.write_videofile(output_directory, codec="libx264")



def create_thumbnail():
    width, height = 500, 500
    background_color = (255, 255, 255)
    image = Image.new("RGB", (width, height), background_color)

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_location, 70)

    today_date = datetime.datetime.now().strftime('%m/%d')

    text_width = draw.textlength(today_date, font=font)
    text_position = ((width - text_width) // 2, (height - font.getlength(today_date)) // 2 + 60)

    draw.text(text_position, today_date, font=font, fill="black")

    image.save(f"today.jpg")