import image_chopper as ic
import XMLreader as r
import time
import helper as h
import os

xml_dir = './labels'
reader = r.XMLreader()
df = reader.read_configs(xml_dir,"*")
print('XML info')
print(df.head())

img_dir = './images'
img_chopper = ic.image_chopper(df,width=150,height = 150)
images = img_chopper.get(img_dir)
print('images')
print(images.iloc[0:2])
h.show(images[0:4])

output_dir = './output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
start_time = time.time()
img_chopper.save(img_dir,output_dir, separate=True)
print('chopping time', time.time()-start_time)
