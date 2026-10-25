"""Build the native crown favicon in SVG, PNG and ICO formats (Pillow)."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]/'assets/logo'
ROOT.mkdir(exist_ok=True,parents=True)
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" role="img" aria-label="The Confident Mind gold crown">
<rect width="96" height="96" rx="22" fill="#0B0B10"/>
<circle cx="48" cy="48" r="42" fill="none" stroke="#9E813C" stroke-width="2.6"/>
<path d="M22 34 32 58H64L74 34 59 44 48 23 37 44Z" fill="#E0C56A"/>
<rect x="32" y="63" width="32" height="5" rx="2" fill="#C9A227"/>
<g fill="#E0C56A"><circle cx="22" cy="31" r="2.5"/><circle cx="48" cy="20" r="2.5"/><circle cx="74" cy="31" r="2.5"/></g>
</svg>
'''
(ROOT/'favicon.svg').write_text(svg)
S=8;im=Image.new('RGBA',(96*S,96*S),(0,0,0,0));d=ImageDraw.Draw(im)
def box(a):return tuple(round(v*S) for v in a)
d.rounded_rectangle(box((0,0,96,96)),radius=22*S,fill='#0B0B10')
d.ellipse(box((6,6,90,90)),outline='#9E813C',width=round(2.6*S))
d.polygon([(x*S,y*S) for x,y in [(22,34),(32,58),(64,58),(74,34),(59,44),(48,23),(37,44)]],fill='#E0C56A')
d.rounded_rectangle(box((32,63,64,68)),radius=2*S,fill='#C9A227')
for x,y in [(22,31),(48,20),(74,31)]:d.ellipse(box((x-2.5,y-2.5,x+2.5,y+2.5)),fill='#E0C56A')
for size,name in [(96,'favicon-96.png'),(180,'apple-touch-icon.png'),(512,'favicon-512.png')]:
    im.resize((size,size),Image.Resampling.LANCZOS).save(ROOT/name)
im.resize((256,256),Image.Resampling.LANCZOS).save(ROOT/'favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64)])
print('SVG, 96px/180px/512px PNG and multi-size ICO written.')
