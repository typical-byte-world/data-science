import scipy.io
import pandas as pd
import numpy as np
import h5py
import tqdm
import json


def get_box_data(index, hdf5_data):
    """
    get 'left, top, width, height' of each picture
    :param index:
    :param hdf5_data:
    :return:
    """
    meta_data = dict()
    meta_data['height'] = []
    meta_data['label'] = []
    meta_data['left'] = []
    meta_data['top'] = []
    meta_data['width'] = []

    def print_attrs(name, obj):
        vals = []
        if obj.shape[0] == 1:
            vals.append(obj[0][0])
        else:
            for k in range(obj.shape[0]):
                vals.append(int(hdf5_data[obj[k][0]][0][0]))
        meta_data[name] = vals

    box = hdf5_data['/digitStruct/bbox'][index]
    hdf5_data[box[0]].visititems(print_attrs)
    return meta_data

def get_name(index, hdf5_data):
    name = hdf5_data['/digitStruct/name']
    return ''.join([chr(v[0]) for v in hdf5_data[name[index][0]].value])



if __name__ == '__main__':
    names = ['extra_digitStruct', 'test_digitStruct', 'train_digitStruct']
    for name_ in names:
        mat_data = h5py.File(name_ + '.mat')
        size = mat_data['/digitStruct/name'].size

        for _i in tqdm.tqdm(range(size)):
            pic = get_name(_i, mat_data)
            box = get_box_data(_i, mat_data)
            print('name', pic, 'box', box)
            
            with open(name_+'.json', 'a') as f:
                json.dump(
                {pic: box},
                f
                )

