# Image Morphing - SIV Project
by Davide Modolo & Edoardo Maines

## Presentation
The [presentation](https://docs.google.com/presentation/d/1DMnK3zVJN2qQJb5nfwMydtcnt2dF2MUdNUQ3A90HNE4/edit?usp=sharing) aims to explain what is Image Morphing and what is it used for. It also explains how our notebook works.

## Jupyter Notebook
### resize.py
Since functions we use require two images of the same size, we wrote a library that edit one or both of them with a minimum (to none) information loss.

### Fading
It starts explaining the easier approach to image morphing: the Fading Effect. It requires two Pillow Images

### Morphing Function
Function to compute the affine transformation steps. It requires two images as numpy array.

### Point-picking
Function to pick by hand three points in each image in order to perform the morph. It requires two images as numpy array.

### Autopick by Template-matching
Look for 3 high-similarity points and morph on them. It requires two images as numpy array.

### Face detection
Using DLIB library and shape_predictor_68_face_landmarks.dat to recognise faces in images and morph. It requires two images as numpy array.

It requires shape_predictor_68_face_landmarks.dat file taken from [here](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

Faces are taken from [This Person Does Not Exist](https://this-person-does-not-exist.com/)

## Anaconda Environment
Since DLIB can easly bring errors, this environment ensures everything works.
