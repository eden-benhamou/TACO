import os.path
import json
import argparse
import numpy as np
import random
import datetime as dt
import copy

parser = argparse.ArgumentParser(description='User args')
parser.add_argument('--dataset_dir', required=True, help='Path to dataset annotations')
#parser.add_argument('--test_percentage', type=int, default=10, required=False, help='Percentage of images used for the testing set')
parser.add_argument('--val_percentage', type=int, default=10, required=False, help='Percentage of images used for the validation set')
parser.add_argument('--nr_trials', type=int, default=1, required=False, help='Number of splits')

args = parser.parse_args()

train_ann_input_path = args.dataset_dir + '/' + 'annotations_train.json'

# Load train annotations
with open(train_ann_input_path, 'r') as f:
    train_dataset = json.loads(f.read())

train_anns = train_dataset['annotations']
#scene_anns = dataset['scene_annotations']
train_imgs = train_dataset['images']
nr_train_images = len(train_imgs)

#nr_testing_images = int(nr_images*args.test_percentage*0.01+0.5)
nr_nontraining_images = int(nr_train_images*(args.val_percentage)*0.01+0.5)


for i in range(args.nr_trials):
    random.shuffle(train_imgs)

    # Add new datasets
    train_set = {'info': train_dataset['info'], 'images': [], 'annotations': [],
                 'licenses': [], 'categories': train_dataset['categories']}

    val_set = copy.deepcopy(train_set)
    test_set = copy.deepcopy(train_set)

    # test_set['images'] = test_dataset['images']
    val_set['images'] = train_imgs[0:nr_nontraining_images]
    train_set['images'] = train_imgs[nr_nontraining_images:nr_train_images]

    # Aux Image Ids to split annotations
    #test_img_ids, val_img_ids, train_img_ids = [],[],[]
    val_img_ids, train_img_ids = [], []
    # for img in test_set['images']:
    #     test_img_ids.append(img['id'])

    for img in val_set['images']:
        val_img_ids.append(img['id'])

    for img in train_set['images']:
        train_img_ids.append(img['id'])

    # Split instance annotations
    for ann in train_anns:
        # if ann['image_id'] in test_img_ids:
        #     test_set['annotations'].append(ann)
        if ann['image_id'] in val_img_ids:
            val_set['annotations'].append(ann)
        elif ann['image_id'] in train_img_ids:
            train_set['annotations'].append(ann)

    # Write dataset splits
    ann_train_out_path = args.dataset_dir + '/' + 'annotations_' + str(i) +'_train.json'
    ann_val_out_path   = args.dataset_dir + '/' + 'annotations_' + str(i) + '_val.json'
    #ann_test_out_path  = args.dataset_dir + '/' + 'annotations_' + str(i) + '_test.json'

    with open(ann_train_out_path, 'w+') as f:
        f.write(json.dumps(train_set))

    with open(ann_val_out_path, 'w+') as f:
        f.write(json.dumps(val_set))

    # with open(ann_test_out_path, 'w+') as f:
    #     f.write(json.dumps(test_set))


