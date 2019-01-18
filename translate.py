
from googletrans import Translator
translator = Translator()
f1=open('friends.srt',"r",encoding="utf-8")
f2=open('hindi2.srt',"a",encoding="utf-8")

for line in f1:
    tr = translator.translate(line, dest='hi')
    print(tr.text)
    f2.write(tr.text+"\n")

f1.close()
f2.close()

import pysrt
subs = pysrt.open('hindi.srt')

from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS 
import os


def speed_swifter(sound, speed):
    return sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})

startmilli=0
s = AudioSegment.silent(duration=0)
for sub in subs:
    diff = (sub.start.hours*3600*1000+sub.start.minutes*60*1000+sub.start.seconds*1000+sub.start.milliseconds)-startmilli
    print(diff)
    s=s+AudioSegment.silent(duration=diff)
    myobj = gTTS(text=sub.text, lang='hi', slow=False)
    myobj.save("voice.mp3")
    vc = AudioSegment.from_mp3('voice.mp3')
    got_len = len(vc)
    ori_len =  (sub.end.hours*3600*1000+sub.end.minutes*60*1000+sub.end.seconds*1000+sub.end.milliseconds) - (sub.start.hours*3600*1000+sub.start.minutes*60*1000+sub.start.seconds*1000+sub.start.milliseconds)
    speed = float(got_len/ori_len)
    sound_with_altered_frame_rate = speed_swifter(vc,speed)
    s=s+sound_with_altered_frame_rate
    startmilli = (sub.end.hours*3600*1000+sub.end.minutes*60*1000+sub.end.seconds*1000+sub.end.milliseconds)

s.export("final_output.mp3",format="mp3")
os.system('del voice.mp3')