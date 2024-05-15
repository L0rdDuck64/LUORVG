from moviepy.editor import *
from pyppeteer import launch
import argostranslate.package
import argostranslate.translate
import autosub
import praw
import random
import asyncio
import edge_tts
import json
import time
import math

print("Loaded API's")

reddit = praw.Reddit(
    client_id='paste your client id here',
    client_secret='paste your client secret here',
    user_agent='LUORVG by L0rdDuck_'
)

subs = ["prorevenge", "pettyrevenge", "nosleep", "talesfromtechsupport", "talesfromretail", "unresolvedmysteries"]

plimit = 500
vidNum = None

#tts setup

VOICES = ['pt-BR-AntonioNeural']
VOICE = VOICES[0]

async def amain(fala, nome) -> None:
    """Main function"""
    communicate = edge_tts.Communicate(fala, VOICE)
    await communicate.save(nome + ".mp3")

# translator

from_code = "en"
to_code = "pt"

# Mp3 thing

def getMp3Lenght(mp3name):
    temp = AudioFileClip(mp3name)

    return temp.duration

# Download and install Argos Translate package

argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

# Moviepy / video editor setup

temps = ["bgtemps/temp1.mp4", "bgtemps/temp2.mp4", "bgtemps/temp3.mp4", "bgtemps/temp4.mp4", "bgtemps/temp5.mp4", "bgtemps/temp6.mp4", "bgtemps/temp7.mp4"]

music = AudioFileClip("resources/musicgou.mp3")
music_duration = music.duration

def split_video(video_clip, num_parts):
    
    if num_parts < 1:
        print("Número de partes deve ser pelo menos 1")
        exit(f"Numero de partes nao é um numero ou menor que 1 ({num_parts})")

    duration = video_clip.duration
    
    part_duration = duration / num_parts
    
    if not os.path.exists("video_parts"):
        os.makedirs("video_parts")

    for part in range(num_parts):
        
        start_time = part * part_duration
        
        if part > 0:
            start_time = max(0, start_time - 1)
        
        end_time = (part + 1) * part_duration
        
        subclip = video_clip.subclip(start_time, end_time)
        
        file_name = f"video_parts/Video{vidNum}Part{part + 1}.mp4"
        
        subclip.write_videofile(file_name, codec="libx264", fps=30, logger=None)

        print(f"Part {part+1} exported")

def repeatVidUntilSecs(video_clip, durat):

    original_duration = video_clip.duration
    
    if original_duration < durat:
        
        repeat_count = int(durat // original_duration) + 1
        
        new_clip = video_clip.loop(repeat_count)

        new_clip = new_clip.set_duration(durat)
    else:
        
        new_clip = video_clip.set_duration(durat)

        print(new_clip.duration)

    return new_clip

def repeatMusicUntilSecs(durat, locMu):

    if music_duration < durat:
    
        MusicReps = int(durat / music_duration) + 1
        locMu = concatenate_audioclips([locMu] * MusicReps)
        locMu = locMu.set_duration(durat)

    elif music_duration > durat:
    
        locMu = locMu.set_duration(durat)
    
    locMu = locMu.volumex(0.01)

    return locMu

# Pyppeter, screenshot handler setup

udd = "C:/Users/username/AppData/Local/Chromium/User Data/Default"

async def take_screenshot(url, output_path, trd): 

    browser = await launch(headless=False, userDataDir=udd)
    page = await browser.newPage()
    
    await page.goto(url)

    await page.waitForSelector('[slot="title"]')

    escpd = json.dumps(trd)[1:-1]

    script = f"""
    
        var titleElement = document.querySelector('[slot="title"]');

        titleElement.innerText = "{escpd}";
    """

    await page.evaluate(script)

    time.sleep(0.7)

    post_title = await page.querySelector('[slot="title"]')

    await page.waitForSelector('[slot="credit-bar"]')

    credit_bar = await page.querySelector('[slot="credit-bar"]')
    
    post_title_box = await post_title.boundingBox()
    credit_bar_box = await credit_bar.boundingBox()
    
    if post_title_box and credit_bar_box:
        post_title_box['x'] -= 15 #10
        post_title_box['y'] -= 20
        post_title_box['width'] += 10 #20
        post_title_box['height'] += 40
        
        credit_bar_box['x'] -= 15
        credit_bar_box['y'] -= 10
        credit_bar_box['width'] += 10
        credit_bar_box['height'] += 20
        
        combined_box = {
            'x': min(post_title_box['x'], credit_bar_box['x']),
            'y': min(post_title_box['y'], credit_bar_box['y']),
            'width': max(post_title_box['x'] + post_title_box['width'], credit_bar_box['x'] + credit_bar_box['width']) - min(post_title_box['x'], credit_bar_box['x']),
            'height': max(post_title_box['y'] + post_title_box['height'], credit_bar_box['y'] + credit_bar_box['height']) - min(post_title_box['y'], credit_bar_box['y'])
        }
        
        
        await page.screenshot({'path': output_path, 'clip': combined_box})
        print("Taked Screenshot from page.")
    else:

        print("Elemento nao encontrado")
    
    await browser.close()

# start of the script


print("Welcome to L0rdDuck_'s Ultimate Op Reddit Video Generator(LUORVG)")

selection = int(input("[ 1. Generate Video ] [ 2. Reset video number ]"))

if selection == 2:
    with open('save.txt', 'w') as arquivo:
            arquivo.write(str(0))
            exit()

srs = int(input("[ 1. Use random sub from table ]"))

if selection == 1:

    if srs == 1:

        chosenSub = random.choice(subs)
        background_video = VideoFileClip(random.choice(temps))

        subreddit = reddit.subreddit(chosenSub)

        vidNum = 0
        with open('save.txt', 'r') as arquivo:
            vidNum = int(arquivo.read()) + 1
        print("Starting Video " + str(vidNum) + " Generation. Getting Messages from sub " + chosenSub)
        posts = [post for post in subreddit.hot(limit=plimit)]
        print("Got posts, using top " + str(plimit) + ", now chosing post from table")
        cpost = random.choice(posts)

        phtitle = cpost.title
        phtext = cpost.selftext

        print("Selected post. Title: " + phtitle)

        print("Translating texts")

        title = argostranslate.translate.translate(phtitle, from_code, to_code)
        text = argostranslate.translate.translate(phtext, from_code, to_code)

        asyncio.get_event_loop().run_until_complete(take_screenshot(cpost.url, "ts.png", title))

        print("Generating Audios...")

        asyncio.run(amain(title, "title"))
        asyncio.run(amain(text, "text"))

        ttlen = math.ceil(getMp3Lenght("title.mp3"))
        etfv = math.ceil(getMp3Lenght("text.mp3") + getMp3Lenght("title.mp3") + 0.75)

        print("Extimated duration for the video: " + str(etfv) + " seconds")
        print("Now select how many parts the video will have(recomended: " + str(math.ceil(etfv / 58)) + ").")

        canProceed = False

        while not canProceed:
            slices = int(input("[ Type the number of parts that you want ]"))

            vidDuration = math.ceil(etfv / slices)

            print("Ok, the duration of each part will be " + str(vidDuration) + " seconds")
            holder = input("If you want to proceed, type Y, else type anything else.")

            if holder.lower() == "y":

                canProceed = True

            else:
                canProceed = False
        
        print("Proceded with " + str(slices) + " parts.")
        print("Now setuping video basics")

        # Setupping bg video and music

        etfv = math.ceil(getMp3Lenght("text.mp3") + getMp3Lenght("title.mp3") + 0.75)

        TrBGv = repeatVidUntilSecs(background_video, etfv)
        music = repeatMusicUntilSecs(etfv, music)

        video = ColorClip(size=(1080, 1920), color=(255,255,255), duration=etfv)

        final_video = CompositeVideoClip([video, TrBGv.set_position(('center', 'center'))])
        final_video = final_video.set_audio(music)

        #SetupEnd

        ttAudio = AudioFileClip("title.mp3")
        txAudio = AudioFileClip("text.mp3")
        whoshAudio = AudioFileClip("resources/whosh.mp3").volumex(0.3)
        sil = AudioFileClip("resources/silence.mp3")

        allAudio = concatenate_audioclips([ttAudio, sil , txAudio])     

        final_video = final_video.set_audio(allAudio)

        timage = ImageClip("ts.png").set_duration(ttlen + 0.5)
        timage = timage.resize(width=1030)
        timage = timage.fx(transfx.fadein, 1)
        timage = timage.fx(transfx.fadeout, 0.5)

        final_video = CompositeVideoClip([final_video, timage.set_position(('center', 750))])

        print("Setupping done")

        trueFV = autosub.generate_subtitles(final_video, ttlen + 0.1)

        allAudio = CompositeAudioClip([music, whoshAudio, allAudio])

        trueFV = trueFV.set_audio(allAudio)

        print("Exporting the parts")

        split_video(trueFV, slices)

        print("all parts exported")

        with open('save.txt', 'w') as arquivo:
            arquivo.write(str(vidNum))