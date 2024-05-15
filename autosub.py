from moviepy.editor import TextClip, CompositeVideoClip
import whisper

def generate_subtitles(video_clip, ignore_seconds):

    print("Started audio extraction for subtitles")

    audio_path = "temp_audio.wav"
    video_clip.audio.write_audiofile(audio_path, logger=None)

    print("Extraction finished, starting subtitle generation")

    model = whisper.load_model("medium")
    audio = whisper.load_audio(audio_path)
    result = model.transcribe(audio)

    subtitle_clips = []
    for segment in result['segments']:
        start_time = segment['start']
        end_time = segment['end']

        if start_time >= ignore_seconds:

            texto = segment['text']
            fontsize = 82

            texto_quebrado = texto  
            
            txt_clip = TextClip(texto_quebrado, fontsize=fontsize, color='black', align='Center', font='NotoSans-Bold', stroke_width=3.2, stroke_color='white', method='caption', size=(1000, 600))

            txt_clip = txt_clip.set_start(start_time).set_duration(end_time - start_time)
            
            txt_clip = txt_clip.set_position(('center', 1040)).set_duration(end_time - start_time)
            subtitle_clips.append(txt_clip)

    video = CompositeVideoClip([video_clip] + subtitle_clips)

    print("Generated Subtitles")

    return video