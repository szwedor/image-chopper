import itertools
import cv2
import os 
import pandas as pd
from toolz import compose,pipe,first

class image_chopper():
    def __init__(self,df,width,height):
        self.df = df
        self._assert()
        self.x = width
        self.y = height
    def _assert(self):
        if not set(['xmin','xmax','ymin','ymax','filename']).issubset(self.df.columns):
            raise Exception('DataFrame is not valid') 
        for extrem, pre in itertools.product(['min','max'],['x','y']):
            self.df[pre+extrem] = pd.to_numeric(self.df[pre+extrem])
    def _get_chopping_fun(self, source_dir):
        x = self.x
        y = self.y
        def chopping_fun(row):
            img = cv2.imread(os.path.join(source_dir, row.filename))
            if img is None:
                print(row.filename,'not found')
                return -1
            crop_img = img[row.ymin:row.ymax, row.xmin:row.xmax]
            border_v = 0
            border_h = 0
            if (y/x) >= (crop_img.shape[0]/crop_img.shape[1]):
                border_v = int((((y/x)*crop_img.shape[1])-crop_img.shape[0])/2)
            else:
                border_h = int((((x/y)*crop_img.shape[0])-crop_img.shape[1])/2)
            crop_img = cv2.copyMakeBorder(crop_img, border_v, border_v, border_h, border_h, cv2.BORDER_CONSTANT, 0)
            crop_img = cv2.resize(crop_img, (x, y))
            return crop_img
        return chopping_fun
    def _validate_dir(self,directory):
        if not os.path.isdir(directory) and not os.path.exists(directory):
            raise Exception('Directory',directory,'does not exists!')
    def get(self, source_dir):
        self._validate_dir(source_dir)
        apply_fun = self._get_chopping_fun(source_dir)
        return self.df.apply(apply_fun, axis = 1)
    def save(self, source_dir, dest_dir, separate = True):
        self._validate_dir(source_dir)
        self._validate_dir(dest_dir)
        chopping_fun = self._get_chopping_fun(source_dir)
        dest_file = lambda row : os.path.join(dest_dir, row.filename)
        if separate:
            paths = [os.path.join(dest_dir, category) for category in self.df.name.unique()]
            [os.makedirs(path) for path in paths if not os.path.exists(path)]
            dest_file = lambda row : os.path.join(dest_dir, row['name'], row['filename'])
        save_fun = lambda row: cv2.imwrite(dest_file(row), chopping_fun(row))
        self.df.apply(save_fun, axis=1)

