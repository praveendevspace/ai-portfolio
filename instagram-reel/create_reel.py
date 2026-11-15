from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, math, wave, struct, json
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parent
TMP=ROOT/'render-assets'; TMP.mkdir(exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe()
W,H=720,1280; FPS=24
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
scenes=[
 ('both','THE DEBATE','Human versus AI. Who really has the edge?', 'Samantha'),
 ('robot','SPEED','I can process text and generate ideas in seconds.', 'Daniel'),
 ('human','LIVED EXPERIENCE','I bring lived experience, feelings, and personal context.', 'Samantha'),
 ('robot','CREATIVITY','I can remix patterns into new possibilities.', 'Daniel'),
 ('human','INTENTION','I bring purpose, taste, and a reason to create.', 'Samantha'),
 ('robot','LIMITS','I can sound confident and still be wrong.', 'Daniel'),
 ('human','JUDGMENT','So I question, verify, and take responsibility.', 'Samantha'),
 ('both','BETTER TOGETHER','The strongest team? Human judgment, with AI assistance.', 'Samantha'),
]
segments=[]
for i,(who,topic,line,voice) in enumerate(scenes):
 a=TMP/f'{i}.aiff'; wav=TMP/f'{i}.wav'
 subprocess.run(['say','-v',voice,'-r','174','-o',str(a),line],check=True)
 subprocess.run([FF,'-y','-loglevel','error','-i',str(a),'-ar','44100','-ac','1','-af','loudnorm=I=-16:TP=-1.5:LRA=11',str(wav)],check=True)
 with wave.open(str(wav),'rb') as f: data=f.readframes(f.getnframes())
 silence=b'\0\0'*int(.55*44100)
 samples=data+silence
 frames=math.ceil(len(samples)/2/44100*FPS)
 samples=samples.ljust(round(frames/FPS*44100)*2,b'\0')
 segments.append((frames,samples))
with wave.open(str(TMP/'dialogue.wav'),'wb') as f:
 f.setparams((1,2,44100,0,'NONE','not compressed'));f.writeframes(b''.join(s[1] for s in segments))
# Original vector-style artwork rendered into animation frames.
bg=Image.new('RGB',(W,H)); pix=bg.load()
for y in range(H):
 for x in range(W):
  glow=max(0,1-math.hypot((x-520)/700,(y-470)/650))
  pix[x,y]=(int(9+8*glow),int(13+12*glow),int(29+21*glow))
def center(d,text,y,size,fill,b=True):
 f=font(size,b); box=d.textbbox((0,0),text,font=f);d.text(((W-(box[2]-box[0]))/2,y),text,font=f,fill=fill)
def wrap(d,text,f,width):
 out=[];line=''
 for word in text.split():
  test=(line+' '+word).strip()
  if d.textlength(test,font=f)>width and line:out.append(line);line=word
  else:line=test
 if line:out.append(line)
 return out
CYAN='#66e8ee';ORANGE='#ffb17c'
def human(d,x,y,active,t):
 bounce=int(math.sin(t*3)*3); y+=bounce
 # shoulders and jacket
 d.rounded_rectangle((x-104,y+77,x+104,y+257),radius=65,fill='#cd7152' if active else '#945541')
 d.polygon([(x-52,y+80),(x,y+150),(x+52,y+80)],fill='#f1dbc0')
 d.rounded_rectangle((x-24,y+48,x+24,y+107),radius=15,fill='#ce936f')
 d.ellipse((x-66,y-90,x+66,y+75),fill='#e8ad86')
 d.pieslice((x-74,y-109,x+70,y+45),180,355,fill='#332a32')
 d.ellipse((x-76,y-56,x-48,y+22),fill='#e8ad86')
 d.ellipse((x+48,y-56,x+76,y+22),fill='#e8ad86')
 blink=math.sin(t*2.2)>.995
 for dx in [-24,24]:
  d.rounded_rectangle((x+dx-5,y-20,x+dx+5,y-17 if blink else y-6),radius=4,fill='#2b2935')
 if active and math.sin(t*20)>-.1:d.ellipse((x-13,y+20,x+13,y+37),fill='#743d3c')
 else:d.arc((x-17,y+10,x+17,y+36),10,170,fill='#743d3c',width=3)
 d.line((x-37,y-35,x-12,y-38),fill='#443037',width=4); d.line((x+12,y-38,x+37,y-35),fill='#443037',width=4)
 # arm gesture
 d.line((x-79,y+142,x-108,y+208),fill='#e8ad86',width=22)
 d.line((x+80,y+145,x+116,y+112+int(math.sin(t*3)*12)),fill='#e8ad86',width=22)
 d.ellipse((x+102,y+96+int(math.sin(t*3)*12),x+132,y+126+int(math.sin(t*3)*12)),fill='#e8ad86')
def robot(d,x,y,active,t):
 y+=int(math.sin(t*2.8+1)*4)
 d.rounded_rectangle((x-99,y+91,x+99,y+257),radius=40,fill='#29505e' if active else '#243c4b',outline='#578593',width=3)
 d.rounded_rectangle((x-25,y+57,x+25,y+103),radius=8,fill='#71939b')
 d.rounded_rectangle((x-80,y-92,x+80,y+70),radius=35,fill='#a4bbc1',outline='#d9eced',width=3)
 d.rounded_rectangle((x-64,y-66,x+64,y+39),radius=22,fill='#102934')
 for dx in [-29,29]:
  d.rounded_rectangle((x+dx-12,y-36,x+dx+12,y-9),radius=8,fill=CYAN if active else '#5babb8')
 for j in range(5):
  h=5+int(abs(math.sin(t*18+j))*14) if active else 5
  d.rounded_rectangle((x-25+j*11,y+13-h//2,x-19+j*11,y+13+h//2),radius=2,fill=CYAN)
 d.line((x,y-93,x,y-125),fill='#95afb7',width=5);d.ellipse((x-9,y-139,x+9,y-121),fill=CYAN)
 d.ellipse((x-25,y+136,x+25,y+186),outline=CYAN,width=3)
 d.ellipse((x-10,y+151,x+10,y+171),fill=CYAN)
 d.line((x-91,y+139,x-118,y+102+int(math.sin(t*3)*10)),fill='#88a9b2',width=19)
 d.ellipse((x-132,y+87+int(math.sin(t*3)*10),x-105,y+115+int(math.sin(t*3)*10)),fill='#bad0d4')
 d.line((x+90,y+143,x+110,y+220),fill='#88a9b2',width=19)

def frame(si,local,globalframe):
 who,topic,line,_=scenes[si];t=globalframe/FPS
 im=bg.copy();d=ImageDraw.Draw(im)
 for x in range(-100,850,90):d.line((x,250,x+200,1000),fill='#1a293d',width=1)
 d.rounded_rectangle((36,52,240,89),radius=18,fill='#263044')
 d.text((52,60),'THE AI CONVERSATION',font=font(13,True),fill='#d0d8e5')
 d.text((493,62),'@hi.aidelulu',font=font(19,True),fill='#d0d8e5')
 center(d,'HUMAN',125,66,ORANGE)
 center(d,'vs. ARTIFICIAL INTELLIGENCE',204,25,'#d5e1ec')
 center(d,topic,284,19,CYAN if who=='robot' else ORANGE if who=='human' else '#f4f1e9')
 # split debate stage
 d.rounded_rectangle((35,356,342,771),radius=25,fill='#20222f',outline=ORANGE if who in ['human','both'] else '#343344',width=2)
 d.rounded_rectangle((378,356,685,771),radius=25,fill='#142936',outline=CYAN if who in ['robot','both'] else '#2e4452',width=2)
 human(d,187,492,who in ['human','both'],t)
 robot(d,531,492,who in ['robot','both'],t)
 d.rounded_rectangle((131,749,244,780),radius=15,fill=ORANGE);d.text((150,756),'HUMAN',font=font(16,True),fill='#281d1c')
 d.rounded_rectangle((489,749,574,780),radius=15,fill=CYAN);d.text((518,756),'AI',font=font(16,True),fill='#102934')
 d.rounded_rectangle((37,830,683,1083),radius=24,fill='#182436',outline='#364356',width=2)
 label='HUMAN + AI' if who=='both' else 'HUMAN SAYS' if who=='human' else 'AI SAYS'
 d.text((64,852),label,font=font(15,True),fill=CYAN if who=='robot' else ORANGE)
 lines=wrap(d,line,font(34,True),582)
 for j,l in enumerate(lines):d.text((64,893+j*44),l,font=font(34,True),fill='#f5f3ee')
 center(d,'Different strengths. Better together.',1120,21,'#d2d9e5')
 center(d,'ANIMATED DEBATE  •  SYNTHETIC VOICES',1160,12,'#7e8da4',False)
 total=sum(n for n,_ in segments);d.rounded_rectangle((42,1212,678,1217),radius=2,fill='#2c3b4f')
 d.rounded_rectangle((42,1212,42+int(636*(globalframe+1)/total),1217),radius=2,fill=CYAN)
 return im
out=ROOT/'human-vs-ai-hi-aidelulu.mp4'
cmd=[FF,'-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(TMP/'dialogue.wav'),'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',str(out)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
g=0;subs=[];elapsed=0
for si,(n,_) in enumerate(segments):
 dur=n/FPS;subs.append({'start':elapsed,'end':elapsed+dur,'speaker':scenes[si][0],'text':scenes[si][2]});elapsed+=dur
 for j in range(n):
  im=frame(si,j,g)
  if si==1 and j==n//2:im.resize((1080,1920)).save(ROOT/'cover.png')
  proc.stdin.write(im.tobytes());g+=1
 print(f'Rendered scene {si+1}/{len(scenes)}',flush=True)
proc.stdin.close()
if proc.wait():raise SystemExit('Video encode failed')
(ROOT/'script.json').write_text(json.dumps(subs,indent=2))
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(subs))+'\n')
(ROOT/'instagram-caption.txt').write_text('Human vs AI: different strengths, better together.\nSpeed and patterns meet lived experience, purpose, and judgment.\nWhich point would you add to this debate?\n\n@hi.aidelulu\n#HumanVsAI #ArtificialIntelligence #AIExplained #FutureOfAI #TechReels\n\nAnimated characters and synthetic voices.\n')
print(json.dumps({'file':str(out),'duration_seconds':elapsed,'frames':g,'width':1080,'height':1920,'fps':FPS,'bytes':out.stat().st_size}))
