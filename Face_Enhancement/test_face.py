# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
from collections import OrderedDict

import data_FE
from options_FE.test_options import TestOptions
from models_FE.pix2pix_model import Pix2PixModel
from util_FE.visualizer import Visualizer
import torchvision.utils as vutils



def test_face(input_opts):
    opt = TestOptions().parse(_input_opts=input_opts)

    dataloader = data_FE.create_dataloader(opt)

    model = Pix2PixModel(opt)
    model.eval()

    visualizer = Visualizer(opt)


    single_save_url = os.path.join(opt.checkpoints_dir, opt.name, opt.results_dir, "each_img")


    if not os.path.exists(single_save_url):
        os.makedirs(single_save_url)


    for i, data_i in enumerate(dataloader):
        if i * opt.batchSize >= opt.how_many:
            break

        generated = model(data_i, mode="inference")

        img_path = data_i["path"]

        for b in range(generated.shape[0]):
            img_name = os.path.split(img_path[b])[-1]
            save_img_url = os.path.join(single_save_url, img_name)

            vutils.save_image((generated[b] + 1) / 2, save_img_url)

