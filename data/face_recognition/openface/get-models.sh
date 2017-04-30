#!/usr/bin/env bash
set -e -x

wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 &&
bunzip2 shape_predictor_68_face_landmarks.dat.bz2

wget http://www.robots.ox.ac.uk/~vgg/software/vgg_face/src/vgg_face_torch.tar.gz &&
tar -xvf vgg_face_torch.tar.gz &&
mv vgg_face_torch/VGG_FACE.t7 ./VGG_FACE.t7 &&
rm -rf vgg_face_torch vgg_face_torch.tar.gz
