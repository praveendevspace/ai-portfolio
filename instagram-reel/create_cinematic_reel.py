"""Render generated movie artwork with camera moves, captions, and existing dialogue."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, json, math
import imageio_ffmpeg
R=Path(__file__).resolve().parent
W,H=720,1280;FPS=24
F='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
font=lambda size:ImageFont.truetype(F,size)
scenes=json.loads((R/'script.json').read_text())
art=Image.open(R/'cinematic-scene.png').convert('RGB')
# Prepare a portrait camera canvas while preserving the generated composition.
ratio=max(W/art.width,H/art.height)
art=art.resize((round(art.width*ratio),round(art.height*ratio)),Image.Resampling.LANCZOS)
left=(art.width-W)//2;top=(art.height-H)//2
art=art.crop((left,top,left+W,top+H))
shade=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(shade)
for y in range(H):
 alpha=int(max(0,1-y/320)*160+max(0,(y-750)/530)*230)
 sd.line((0,y,W,y),fill=(3,9,16,min(245,alpha)))
def wrap(d,text,f,width):
 result=[];line=''
 for word in text.split():
  test=(line+' '+word).strip()
  if d.textlength(test,font=f)>width and line:result.append(line);line=word
  else:line=test
 if line:result.append(line)
 return result
def center(d,text,y,size,fill):
 f=font(size);tw=d.textlength(text,font=f);d.text(((W-tw)/2,y),text,font=f,fill=fill,stroke_width=1,stroke_fill='#000000')
ff=imageio_ffmpeg.get_ffmpeg_exe();out=R/'human-vs-ai-cinematic-hi-aidelulu.mp4'
proc=subprocess.Popen([ff,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(R/'render-assets/dialogue.wav'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=3dB,alimiter=limit=0.95:level=false','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-ac','2','-b:a','192k','-movflags','+faststart','-shortest',str(out)],stdin=subprocess.PIPE)
total=round(scenes[-1]['end']*FPS)
for si,s in enumerate(scenes):
 start=round(s['start']*FPS);end=round(s['end']*FPS);n=end-start
 for j in range(n):
  progress=j/max(1,n-1)
  zoom=1.01+.055*progress if si%2==0 else 1.065-.04*progress
  cw,ch=W/zoom,H/zoom
  target=.37 if s['speaker']=='human' else .63 if s['speaker']=='robot' else .5
  x=max(0,min(W-cw,W*target-cw/2));y=(H-ch)*.40
  im=art.transform((W,H),Image.Transform.EXTENT,(x,y,x+cw,y+ch),Image.Resampling.BICUBIC).convert('RGBA')
  im=Image.alpha_composite(im,shade);d=ImageDraw.Draw(im)
  d.text((44,65),'A CONVERSATION ABOUT THE FUTURE',font=font(13),fill='#d9d9d3')
  center(d,'HUMAN / AI',116,56,'#fff5df')
  center(d,'@hi.aidelulu',188,19,'#e8cba1')
  who='HUMAN + AI' if s['speaker']=='both' else s['speaker'].upper()
  color='#ffd3a4' if s['speaker']=='human' else '#9eeaf0' if s['speaker']=='robot' else '#e8d4b4'
  d.rounded_rectangle((44,895,210,930),radius=5,fill='#10232ce0',outline=color)
  d.text((58,904),who,font=font(15),fill=color)
  lines=wrap(d,s['text'],font(32),620)
  for k,line in enumerate(lines):d.text((44,959+43*k),line,font=font(32),fill='#fff9ef',stroke_width=1,stroke_fill='#050a0f')
  d.text((44,1150),'DIFFERENT STRENGTHS. BETTER TOGETHER.',font=font(15),fill='#d4d5d2')
  d.text((44,1187),'AI-GENERATED VISUAL • SYNTHETIC VOICES',font=font(11),fill='#a8b4bc')
  d.rectangle((44,1225,676,1228),fill='#445460')
  d.rectangle((44,1225,44+int(632*(start+j+1)/total),1228),fill=color)
  im=im.convert('RGB')
  if si==0 and j==n//2:im.resize((1080,1920)).save(R/'cinematic-cover.png')
  proc.stdin.write(im.tobytes())
 print(f'Rendered cinematic scene {si+1}/8',flush=True)
proc.stdin.close()
if proc.wait():raise SystemExit('Encoding failed')
print(out)
