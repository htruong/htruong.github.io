# A coffee ring taken from Nevit Dilmen's photo of a real one (CC BY-SA 3.0):
# the stain is the yellow in the picture, so its density is read from the
# chroma (how much less blue than red/green each pixel is), which leaves out
# the paper towel's grey emboss. Written out as coffee colour with that density
# as alpha, to be multiplied onto the printout.
from PIL import Image, ImageFilter
import numpy as np
im=Image.open('../full/ring-towel.jpg').convert('RGB')
a=np.asarray(im).astype(float)
yel=(a[...,0]+a[...,1])/2-a[...,2]
bg=np.median(yel)
d=np.clip(yel-bg-4,0,None)
print('bg',bg,'p99',np.percentile(d,99.5))
d=d/np.percentile(d,99.7)
d=np.clip(d,0,1)
m=Image.fromarray((d*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2))
m.save('stain-density.png')
m.resize((768,576)).save('stain-density-small.png')

# keep the ring, drop the faint streaks of shading inside it, crop it square
d=np.asarray(m).astype(float)/255
d=np.clip((d-0.18)/0.82,0,1)**1.15
cx,cy,r=1700,1100,1060
d=d[cy-r:cy+r, cx-r:cx+r]
# colour: dried coffee, the brown of a dried ring

col=(128,72,22)
out=np.zeros(d.shape+(4,),np.uint8); out[...,0],out[...,1],out[...,2]=col
out[...,3]=(np.clip(d*0.95,0,1)*255).astype(np.uint8)
o=Image.fromarray(out,'RGBA').resize((420,420),Image.LANCZOS)
import sys; o.save(sys.argv[1] if len(sys.argv)>1 else 'coffee-ring.webp','WEBP',quality=85,method=6)
bg=Image.new('RGB',o.size,(248,247,240)); bg.paste(o,(0,0),o); bg.save('coffee-ring-preview.png')
