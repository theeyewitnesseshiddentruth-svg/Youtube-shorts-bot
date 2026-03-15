from gtts import gTTS

def create_voice(script, filename="voice.mp3"):
    tts = gTTS(script)
    tts.save(filename)
    return filename
