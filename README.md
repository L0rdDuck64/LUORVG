# LUORVG
L0rdDuck's Ultimate Op Reddit Video Generator(LUORVG) isn't a reddit video generator tool 😨

Supports shorts video generation

#### ⚠ The project is very incomplete and have few features ⚠

## Info

Made in python  
Generator languages: pt-br  
Uses moviepy  
The file [save.txt](./save.txt) is the video counter, you can just edit it to change the video number or use the option to reset it when running the program.

#### Maybe you want to change the codec to nvenc_h264 in [main.py](./main.py) if you have a nvidia GPU for faster encoding

## Requirements

`pip install moviepy`  
`pip install openai-whisper`  
`pip install praw`  
`pip install argostranslate`  
`pip install pyppeteer`  
`pip install asyncio`  
`pip install edge-tts`  

You also need to install chromium and log into your reddit account, after that you need to get the User Data Directory going to [chrome://version](chrome://version/) in chromium, copy the UDD and paste at line 134.  

Also edit the praw configs client id and client secret at line 16 by your app client id and secret.

## Basics

Run main.py and select the options to generate the video, exported videos go to video_parts folder.  

There will be some videos in bgtemps folder, but if you wanna add them manually check [videos.md](./bgtemps/videos.md)  

## Downloading

Just download from releases I think.

## Common issues

#### Why Im getting a error about resizing a ImageClip?

Probably its because moviepy use a deprecated method in pillow to resize images, to fix this run this command:  
`pip install Pillow==9.5.0`

## A next project

Since LUORVG is pretty incomplete and it needs more features, Im planning doing a new version called LUORVG 2 or smth. This new version will get lots of features, like:  

* Automatic video generation(generates more than 1 video per time)
* More options to choose
* Option to choose a custom subreddit
* Large videos generation
* Automate video type by story size
* And much more!(Im lazy to describe everything here and there is somethings that I didn't confirmed yet)