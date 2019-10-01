import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import tkinter
import coco
import utils
import model as modellib
import visualize

import torch
import argparse



if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--images', required=False,
                        default="images",
                        help='Directory of the images')
    
    parser.add_argument('--weights', required=False,
                        default="mask_rcnn_coco_0160.pth",
                        help="Path to weights .pth file or 'coco'")

    args = parser.parse_args()


    # Root directory of the project
    ROOT_DIR = os.getcwd()

    # Directory to save logs and trained model
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")

    # Path to trained weights file
    # Download this file and place in the root of your
    # project (See README file for details)
    COCO_MODEL_PATH = os.path.join(ROOT_DIR, args.weights)

    # Directory of images to run detection on
    IMAGE_DIR = os.path.join(ROOT_DIR, args.images)

    class InferenceConfig(coco.CocoConfig):
        # Set batch size to 1 since we'll be running inference on
        # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
        # GPU_COUNT = 0 for CPU
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        NUM_CLASSES = 4

    config = InferenceConfig()
    config.display()

    # Create model object.
    model = modellib.MaskRCNN(model_dir=MODEL_DIR, config=config)
    if config.GPU_COUNT:
        model = model.cuda()

    # Load weights trained on MS-COCO
    model.load_state_dict(torch.load(COCO_MODEL_PATH))

    # COCO Class names
    # Index of the class in the list is its ID. For example, to get ID of
    # the teddy bear class, use: class_names.index('teddy bear')
    class_names = ['BG','wet_tissue','food_wrap','steel_scourer']

    # Load a random image from the images folder
    file_names = next(os.walk(IMAGE_DIR))[2]
    image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))

    # Run detection

    results = model.detect([image])

    # Visualize results
    matplotlib.use('TkAgg')
    r = results[0]
    visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                           class_names, r['scores'])
    plt.show()
