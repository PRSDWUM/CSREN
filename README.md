# CSREN
Cross-Modal Semantic Relations Enhancement With Graph Attention Network for Image-Text Matching
# Introduction
This is the source code of Cross-Modal Semantic Relations Enhancement With Graph Attention Network for Image-Text Matching(CSREN), a novel approch for Image-Text matching. It is built on top of the SCAN ([Stacked cross attention for image-text matching by Kuang-Huei Lee](https://github.com/kuanghuei/SCAN)) in PyTorch.
# Requirements and Installation
We recommended the following dependencies:
<br>* Python 3.8
<br>* PyTorch 2.0
<br>* NumPy 1.20.0
<!-- <br>* TensorBoard -->
# Download data
We use the dataset files as SCAN([Stacked cross attention for image-text matching by Kuang-Huei Lee](https://github.com/kuanghuei/SCAN)) , initializing each text word with the BERT base model.
# Training new models
To train Flickr30K and MS-COCO models:
<br>* python train.py
