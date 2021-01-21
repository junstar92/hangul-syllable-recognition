# -*- coding: utf-8 -*-
import tensorflow as tf
import os
import json

class MyCallback(tf.keras.callbacks.Callback):
    def __init__(self, opt):
        self.opt = opt
        self.max_acc = -1
        self.min_loss = 100000
        
    def on_epoch_end(self, epoch, logs={}):
        val_acc = logs.get('val_acc')
        val_loss = logs.get('val_loss')
        
        if os.path.isdir(self.opt.save_path) == False:
            os.mkdir(self.opt.save_path)
        
        self.model.save_weights(os.path.join(self.opt.save_path, f'{epoch+1}_epoch_model.h5'))
        
        if val_acc is not None:
            if val_acc > self.max_acc:
                print('\n--- save best acc model weights ---')
                self.max_acc = val_acc
                self.model.save_weights(os.path.join(self.opt.save_path, f'best_acc_{logs.get("val_acc"):.2f}_model.h5'))
                
            if logs.get('val_acc') >= 0.99:
                print('Reach 99% validation accuracy !')
        
        if val_loss is not None:
            if val_loss < self.min_loss:
                print('\n--- save best loss model weights ---')
                self.min_loss = val_loss
                self.model.save_weights(os.path.join(self.opt.save_path, f'best_loss_{logs.get("val_loss"):.2f}_model.h5'))
                

def getImageAndLabelFromJson(path, json_path, character):
    #file_paths = [os.path.join(path, f'{file}') for file in files]
    file_paths = []
    labels = []
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data_json = json.load(f)
        
        for data in data_json['annotations']:
            if data['attributes']['type'] == '글자(음절)':
                file = os.path.join(path, f"{data['image_id']}.png")
                if os.path.exists(file) and data['text'] in character:
                    file_paths.append(file)
                    #if data['text'] in character:
                    labels.append(data['text'])
                    #else:
                    #    labels.append('?')
    
    return file_paths, labels

if __name__ == '__main__':
    path = './data/AI_HUB/printed_data_info.json'
    with open(path, 'r', encoding='utf-8') as f:
        data_json = json.load(f)
    print(data_json['annotations'][546938])