# -*- coding: utf-8 -*-
import tensorflow as tf

def VGG_FeatureExtractor(num_class, input_shape=(32,32,3), output_channel=512):
    output_channel = [int(output_channel / 8), int(output_channel / 4),
                      int(output_channel / 2), output_channel] # [64, 128, 256, 521]
    inputs = tf.keras.layers.Input(input_shape) # 32x32x3
    outputs = tf.keras.layers.Conv2D(output_channel[0], 3, padding='same', activation='relu')(inputs) # 32x32x64
    outputs = tf.keras.layers.MaxPooling2D(2, 2)(outputs) # 16x16x64
    outputs = tf.keras.layers.Conv2D(output_channel[1], 3, padding='same', activation='relu')(outputs) # 16x16x128
    outputs = tf.keras.layers.MaxPooling2D(2, 2)(outputs) # 8x8x128
    outputs = tf.keras.layers.Conv2D(output_channel[2], 3, padding='same', activation='relu')(outputs) # 8x8x256
    outputs = tf.keras.layers.Conv2D(output_channel[2], 3, padding='same', activation='relu')(outputs) # 8x8x256
    outputs = tf.keras.layers.MaxPooling2D(2, 2)(outputs) # 4x4x256
    outputs = tf.keras.layers.Conv2D(output_channel[3], 3, padding='same', activation='relu', use_bias=False)(outputs) # 4x4x512
    outputs = tf.keras.layers.BatchNormalization()(outputs)
    outputs = tf.keras.layers.ReLU()(outputs)
    outputs = tf.keras.layers.Conv2D(output_channel[3], 3, padding='same', activation='relu', use_bias=False)(outputs) # 4x4x512
    outputs = tf.keras.layers.BatchNormalization()(outputs)
    outputs = tf.keras.layers.ReLU()(outputs)
    outputs = tf.keras.layers.MaxPooling2D(2, 2)(outputs) # 2x2x512
    outputs = tf.keras.layers.Flatten()(outputs) # 2048
    outputs = tf.keras.layers.Dropout(0.3)(outputs)
    outputs = tf.keras.layers.Dense(num_class, activation='softmax')(outputs)
    
    model = tf.keras.models.Model(inputs=inputs, outputs=outputs)
    
    return model