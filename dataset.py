# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import argparse
import random

class DataGenerator(tf.keras.utils.Sequence):
    def __init__(self, data_path, opt, shuffle=True, train=True):
        self.path = data_path
        self.file_names = os.listdir(data_path)
        self.n_samples = len(self.file_names)
        #random.shuffle(self.file_names)
        self.shuffle=shuffle
        self.train=train
        
        self.batch_size = opt.batch_size
        self.num_class = len(opt.character)
        
        self.idx_to_char = list(opt.character)
        self.char_to_idx = {}
        for i, char in enumerate(self.idx_to_char):
            self.char_to_idx[char] = i
            
        self.on_epoch_end()
        print(f'{self.n_samples} images loaded')
    
    def __len__(self):
        return int(np.floor(self.n_samples / self.batch_size))
    
    def on_epoch_end(self):
        self.indices = np.arange(self.n_samples)
        if self.shuffle:
            np.random.shuffle(self.indices)
    
    def __getitem__(self, index):
        indices = self.indices[index*self.batch_size:(index+1)*self.batch_size]
        files = [self.file_names[i] for i in indices]#range(index*self.batch_size, (index+1)*self.batch_size)]
        xs = []
        ys = []
        
        for file in files:
            x = load_img(os.path.join(self.path, file), target_size=(32,32))
            x = img_to_array(x)
            x = x / 255.
            xs.append(x)
            
            if self.train == True:
                label = file[0]
                ys.append(self.char_to_idx[label])
        
        return np.array(xs), np.array(ys)
        
class DataGeneratorByPath(tf.keras.utils.Sequence):
    def __init__(self, file_paths, labels, opt, shuffle=True):
        self.file_paths = file_paths
        self.labels = labels
        self.batch_size = opt.batch_size
        self.shuffle = shuffle
        
        self.idx_to_char = list(opt.character)#['?'] + list(opt.character)
        self.char_to_idx = {}
        for i, char in enumerate(self.idx_to_char):
            self.char_to_idx[char] = i#+1
        #self.char_to_idx[self.idx_to_char[0]] = 0
        
        self.num_class = len(self.idx_to_char)
        self.n_samples = len(self.file_paths)
        
        self.on_epoch_end()
        print(f'{self.n_samples} images loaded')
    
    def __len__(self):
        return int(np.floor(self.n_samples / self.batch_size))
    
    def on_epoch_end(self):
        self.indices = np.arange(self.n_samples)
        if self.shuffle:
            np.random.shuffle(self.indices)
    
    def __getitem__(self, index):
        indices = self.indices[index*self.batch_size:(index+1)*self.batch_size]
        files = [self.file_paths[i] for i in indices]
        labels = [self.labels[i] for i in indices]
        xs = []
        ys = []
        
        for file, label in zip(files, labels):
            x = load_img(file, target_size=(32,32))
            x = img_to_array(x)
            x = x / 255.
            xs.append(x)
            
            ys.append(self.char_to_idx[label])
        
        return np.array(xs), np.array(ys)