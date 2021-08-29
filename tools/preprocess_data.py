import argparse
import os
import random
import re

import pandas as pd

now_path = os.getcwd()
father_path = os.path.abspath(os.path.dirname(now_path) + os.path.sep + '.')
grandfather_path = os.path.abspath(os.path.dirname(father_path) + os.path.sep + '.')


def extract_pos_data(data_file):
    holiwood_data = data_file
    holiwood_file = []
    pto_file = []
    holiwood_object = []
    holiwood_bbox = []
    holiwood_scale = []
    long_num = 0

    with open(holiwood_data) as f:
        for eachline in f.readlines():
            eachline = eachline.split('\n')[0]
            if re.match(r'###', eachline):
                long_num += 1
            elif re.match(r'file:', eachline):
                holiwood_file.insert(len(holiwood_file), father_path + '/dataset/holiwood/' + eachline[6:])
                pto_file.insert(len(pto_file), father_path + '/dataset/holiwood/' + eachline[6:])
            elif re.match(r'object:', eachline):
                holiwood_object.insert(len(holiwood_object), int(eachline[8:]))
                if len(holiwood_object) > len(holiwood_file):
                    holiwood_file.insert(len(holiwood_file), holiwood_file[len(holiwood_file) - 1])
            elif re.match(r'bbox:', eachline):
                holiwood_bbox.insert(len(holiwood_bbox), eachline[6:])
            elif re.match(r'scale:', eachline):
                holiwood_scale.insert(len(holiwood_scale), eachline[7:])
            else:
                continue

    return [holiwood_file, pto_file, holiwood_bbox]


def save_as_txt(file_name, label, bbox_xz=0, bbox_yz=0, bbox_xy=0, bbox_yy=0, path_txt=None):
    data = {"file_name": file_name, 'label': label, 'bbox_xz': bbox_xz, 'bbox_yz': bbox_yz, 'bbox_xy': bbox_xy,
            'bbox_yy': bbox_yy}
    df = pd.DataFrame(data)
    df.to_csv(path_txt, sep=',', index=False, encoding='utf-8-sig')


def pos_data(file_name, pto_file, bbox, save_file):
    path_txt = save_file
    train_file = []
    train_bbox_xz = []
    train_bbox_yz = []
    train_bbox_xy = []
    train_bbox_yy = []
    train_label = []
    test_file = []
    test_bbox_xz = []
    test_bbox_yz = []
    test_bbox_xy = []
    test_bbox_yy = []
    test_label = []
    random_index = list(range(0, 1120))

    temp_train_index = random.sample(random_index, 720)

    for index in temp_train_index:
        for i in range(len(file_name)):
            if file_name[i] == pto_file[index]:
                train_file.append(file_name[i])
                bbox_xyxy = bboxstr2list(bbox[i])
                train_bbox_xz.append(bbox_xyxy[0])
                train_bbox_yz.append(bbox_xyxy[1])
                train_bbox_xy.append(bbox_xyxy[2])
                train_bbox_yy.append(bbox_xyxy[3])
                train_label.append(0)
        random_index.remove(index)
    save_as_txt(train_file, train_label, train_bbox_xz, train_bbox_yz, train_bbox_xy, train_bbox_yy,
                (path_txt + 'train.txt'))

    for index in random_index:
        for i in range(len(file_name)):
            if file_name[i] == pto_file[index]:
                test_file.append(file_name[i])
                bbox_xyxy = bboxstr2list(bbox[i])
                test_bbox_xz.append(bbox_xyxy[0])
                test_bbox_yz.append(bbox_xyxy[1])
                test_bbox_xy.append(bbox_xyxy[2])
                test_bbox_yy.append(bbox_xyxy[3])
                test_label.append(0)
    save_as_txt(test_file, test_label, test_bbox_xz, test_bbox_yz, test_bbox_xy, test_bbox_yy, (path_txt + 'test.txt'))


def bboxstr2list(bbox_str):
    temp_xywh = []
    bbox_str = bbox_str.split('\n')[0]
    for j in bbox_str.split(','):
        temp_xywh.append(float(j))
    temp_xyxy = [temp_xywh[0], temp_xywh[1], temp_xywh[0] + temp_xywh[2],
                 temp_xywh[1] + temp_xywh[3]]
    return temp_xyxy


def main():
    parse = argparse.ArgumentParser(
        description='preprocess data')
    parse.add_argument('--holiwood_data',
                       type=str, default=father_path + '/dataset/holiwood/head_stats.txt')
    parse.add_argument('--pos_path_txt', type=str,
                       default=father_path + '/dataset/pos/')
    args = parse.parse_args()

    file_name, pto_file, bbox = extract_pos_data(args.holiwood_data)
    pos_data(file_name=file_name, pto_file=pto_file, bbox=bbox, save_file=args.pos_path_txt)


if __name__ == '__main__':
    main()
