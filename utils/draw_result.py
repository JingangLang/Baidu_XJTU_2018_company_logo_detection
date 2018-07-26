import os
import shutil
import colorsys
from PIL import Image, ImageDraw, ImageFont


import numpy as np
import pandas as pd


from tqdm import tqdm


mapping_list = pd.read_csv('./class_name.csv', header=None, names=['abbr', 'fullname'])  # 类编号-类名映射


# 随机生成颜色
hsv_tuples = [(x / 60, 1., 1.)
                      for x in range(60)]  # 60 classes
colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                colors))
np.random.seed(10101)  # Fixed seed for consistent colors across runs.
np.random.shuffle(colors)  # Shuffle colors to decorrelate adjacent classes.
np.random.seed(None)  # Reset seed to default.


def init():

    if os.path.exists('../result_vis'):
        for _, _, files in os.walk('../result_vis'):
            for file in files:
                os.remove('../result_vis/' + file)
        os.rmdir('../result_vis')

    os.mkdir('../result_vis')

    for _, _, files in os.walk('../../data/test'):
        for file in files:
            shutil.copy('../../data/test/' + file, '../result_vis/' + file)


def plot_box(row):

    image = Image.open('../result_vis/' + row['filename'])
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font='../font/FiraMono-Medium.otf',
                              size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))

    thickness = (image.size[0] + image.size[1]) // 300

    # print(row['claz'], (row['x_min'], row['y_min']), (row['x_max'], row['y_max']))

    for i in range(thickness):
        draw.rectangle(
            [row['x_min'] + i, row['y_min'] + i, row['x_max'] - i, row['y_max']- i],
            outline=colors[int(row['claz'])-1])

    label = '{} {:.2f}'.format(mapping_list.loc[row['claz'], 'abbr'], row['score'])
    label_size = draw.textsize(label, font)
    if row['y_min'] - label_size[1] >= 0:
        text_origin = np.array([row['x_min'], row['y_min'] - label_size[1]])
    else:
        text_origin = np.array([row['x_min'], row['y_min'] + 1])

    draw.rectangle(
        [tuple(text_origin), tuple(text_origin + label_size)],
        fill=colors[int(row['claz'])-1])
    draw.text(text_origin, label, fill=(0, 0, 0), font=font)

    image.save('../result_vis/' + row['filename'])


init()

result_list = pd.read_csv('../result/960_0.1_0.6_YOLOv3.csv', sep=' ', header=None, index_col=False, names=['filename', 'claz', 'score', 'x_min', 'y_min', 'x_max', 'y_max'])
for i in tqdm(range(len(result_list))):
    plot_box(result_list.iloc[i])

