# <img src="README/icon.png" width="20"> SiamBOMB

[![License](https://img.shields.io/badge/License-Apache%202.0-brightgreen.svg)](https://github.com/JackieZhai/SiamBOMB/blob/master/LICENSE)
![RepoSize](https://img.shields.io/github/repo-size/JackieZhai/SiamBOMBPro)
![CodeSize](https://img.shields.io/github/languages/code-size/JackieZhai/SiamBOMBPro)
[![Release](https://img.shields.io/github/v/release/JackieZhai/SiamBOMBPro?include_prereleases&sort=semver)](https://github.com/JackieZhai/SiamBOMBPro/releases)
![Commit](https://img.shields.io/github/last-commit/JackieZhai/SiamBOMBPro)

This repo is preview version 0.2 of SiamBOMB. \
Copyright \(c\) 2020 Institute of Automation, Chinese Academy of Sciences. 
All rights reserved.
<p align="center"><img src="README/affiliation.png" width="500"></p>

## Introduction
Our Demo Video: [https://youtu.be/x4tjOdrtQ98](https://youtu.be/x4tjOdrtQ98) or [https://www.bilibili.com/video/av92152869](https://www.bilibili.com/video/av92152869) \
Our Paper (IJCAI 2020 Demo Track): [10.24963/ijcai.2020/776](https://www.ijcai.org/Proceedings/2020/0776.pdf) \
Demo from [Ziegler et al.](https://zenodo.org/record/3608658)

<p align="center"><img src="README/demo.gif" width="500"></p>

1. This project is based on [PySOT](https://github.com/STVIR/pysot).
2. We develop it with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro).
3. It can import images, video and webcam.
4. It can setting multiple tracking objects.
5. It can do fundamental behavioral analysis and save data.
## Setup
### 1. Configure environments
* Linux (Ubuntu 18.04) or Windows (10).
* GPU (at least have 4 GB memory).
* CUDA 10.1 (with cuDNN).
* Anaconda 4.8+ (or virtualenv etc.).
* Download .zip or `git clone` our code.
### 2. Install dependencies
```Shell
# create anaconda env
conda create -n SiamBOMB python=3.6
conda activate SiamBOMB

# install the pytorch
conda install pytorch torchvision cudatoolkit=10.1 -c pytorch

# install the pyqt5
pip install pyqt5-tools

# install other packages
pip install numpy opencv-python pyyaml yacs tqdm colorama matplotlib cython tensorboardX

# build extensions
python setup.py build_ext --inplace
```
### 3. Equip models
A simple SiamMask pretrained model: \
[Google Drive](https://drive.google.com/file/d/1VVpCAUJeysyRWdLdfW1IsT3AsQUQvwAU/view), [Baidu Pan](https://pan.baidu.com/s/1q64A2jPEWmdj264XrfvhBA) (key: jffj) \
You need to copy it into `pysot/experiments/siammaske_r50_l3/`.\
You can also choose other models from: [Model Zoo](https://github.com/STVIR/pysot/blob/master/MODEL_ZOO.md) (need to modify codes).
## Demo
```Shell
python window_running.py
```
1. [Top three buttons] Choose one of three loading ways: images, video or webcam.

<p align="center"><img src="README/demo1.png" width="150"></p>

2. [B-box setting] Select several bounding for your targets and determine which is the first frame, it can re-select. 
(Using the Mouse and Keyboard ',' and '.' or bottom-right ScrollBar)

<p align="center"><img src="README/demo2.png" width="150"> <img src="README/demo7.png" width="200"></p>

3. [Algorithm processing] Do tracking and segmentation, press [...Suspending] if you want to terminate.

<p align="center"><img src="README/demo3.png" width="150">
<img src="README/demo8.png" width="155"></p>

* Bottom-left is Status/ProcessBar.

<p align="center"><img src="README/demo6.png" width="400"></p>

* Top-left shows output messages including Behavior Analysis. Middle-Right SpinBox for selecting from multiple target.

<p align="center"><img src="README/demo4.png" width="190"></p>

* Middle-Right CheckBox for saving data locally. You can use bottom-right ScrollBar for review after Algorithm procedure.

<p align="center"><img src="README/demo5.png" width="120"></p>

* Suitable for any size of image stream which is smaller than projection area (you can rescale the window before loading stream).
The results are saved in the path of `ans`.

## Citation
```
@inproceedings{SiamBOMB,
  title     = {SiamBOMB: A Real-time AI-based System for Home-cage Animal Tracking, Segmentation and Behavioral Analysis},
  author    = {Chen, Xi and Zhai, Hao and Liu, Danqian and Li, Weifu and Ding, Chaoyue and Xie, Qiwei and Han, Hua},
  booktitle = {Proceedings of the Twenty-Ninth International Joint Conference on
               Artificial Intelligence, {IJCAI-20}},
  publisher = {International Joint Conferences on Artificial Intelligence Organization},             
  pages     = {5300--5302},
  year      = {2020},
  month     = {7},
  doi       = {10.24963/ijcai.2020/776},
  url       = {https://doi.org/10.24963/ijcai.2020/776},
}
```

## References
### Repositories
[PySOT](https://github.com/STVIR/pysot), 
[SiamFC](https://github.com/huanglianghua/siamfc-pytorch), 
[SiamRPN](https://github.com/foolwood/DaSiamRPN), 
[SiamMask](https://github.com/foolwood/SiamMask), 
[THOR](https://github.com/xl-sr/THOR), 
[SiamMask_E](https://github.com/baoxinchen/siammask_e), 
[SiamDW](https://github.com/researchmm/SiamDW)
### Papers
```
@inproceedings{SiamMask,
  title={Fast online object tracking and segmentation: A unifying approach},
  author={Wang, Qiang and Zhang, Li and Bertinetto, Luca and Hu, Weiming and Torr, Philip HS},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={1328--1338},
  year={2019}
}

@article{SiamMask_E,
  title={Fast visual object tracking with rotated bounding boxes},
  author={Chen, Bao Xin and Tsotsos, John K},
  journal={arXiv preprint arXiv:1907.03892},
  year={2019}
}

@article{THOR,
  title={Tracking Holistic Object Representations},
  author={Sauer, Axel and Aljalbout, Elie and Haddadin, Sami},
  journal={arXiv preprint arXiv:1907.12920},
  year={2019}
}

@article{A_Common_Hub,
  title={A common hub for sleep and motor control in the substantia nigra},
  author={Liu, Danqian and Li, Weifu and Ma, Chenyan and Zheng, Weitong and Yao, Yuanyuan and Tso, Chak Foon and Zhong, Peng and Chen, Xi and Song, Jun Ho and Choi, Woochul and others},
  journal={Science},
  volume={367},
  number={6476},
  pages={440--445},
  year={2020},
  publisher={American Association for the Advancement of Science}
}
```
