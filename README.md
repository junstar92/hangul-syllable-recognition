# hangul-syllable-recognition

## Introduction

한글은 조합이 다양하기 때문에 영어에 비해서 OCR 성능이 조금 떨어진다고 알고 있다. 

다양한 폰트와 손글씨 데이터를 가지고, 얼마나 한글을 잘 인식하는지 확인하기 위해서 프로젝트를 진행했다.

## Getting started
### Training Data

프로젝트를 위한 Data는 총 두 종류의 Data를 사용했다. 

TextRecognitionDataGenerator로 생성한 글자 이미지 100,000장과 AI Hub에서 제공하는 글자 이미지 404,474장을 사용했다.

#### TextRecognitionDataGenerator

Github : https://github.com/Belval/TextRecognitionDataGenerator

font파일과 생성할 글자들을 모은 txt파일이 있으면, 위의 TextRecognitionDataGenerator를 통해서 글자 이미지를 생성할 수 있다.

1. fonts/ko에 font 추가(.ttf파일)
- 생성에 사용된 font는 기본으로 사용되는 font와 네이버에서 제공되는 손끌씨 font이며, 그 목록은 다음과 같다.
    <img src="./documents/font_list.png">


2. dicts/ko에 학습용 글자 음절 추가(.txt파일)
- 사용되는 글자는 KS X 1001 완성형에 포함된 현대 한글 2350자를 사용하였다.
	<img src="./documents/syllable_list.png">

<img src="./documents/generated_data.png">

#### AI Hub

Link : https://aihub.or.kr/aidata/133

<img src="./documents/AI_Hub_page.png">

AI Hub에서 현대 한글 11,172자를 가장 많이 활용하는 폰트 50종을 선정하여 학습용 이미지와 어노테이션을 제공한다. 또한, 손글씨도 제공하는데, 연령층별로 손글씨 작성인력을 확보해 직접 작성 제작한 손글씨 이미지와 어노테이션을 제공한다. 

조합할 수 있는 모든 한글에 대한 이미지가 존재하기 때문에, 전처리 과정을 통해서 사용할 2,350자에 대한 이미지 경로만 추출하여서 학습에 사용했다.


### Create dataset

Data는 이미지의 경로와 라벨을 csv파일에 저장하였고, csv파일을 읽어서 Train/Valid Dataset을 생성하였다.

Datatset 생성 과정에서 이미지의 크기를 32px x 32px로 resize하고, pixel값이 [0, 1]의 값을 갖도록 normalization을 적용해주었다. (datasets.py)

