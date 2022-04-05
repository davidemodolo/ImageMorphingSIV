from PIL import Image
import numpy as np
from matplotlib import cm
import cv2
import math


def normalizeImages(img1, img2):
    img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_BGR2RGB)

    img1 = Image.fromarray(img1.astype('uint8'), 'RGB')
    img2 = Image.fromarray(img2.astype('uint8'), 'RGB')
    # first case: images already have the same size
    if(img1.size == img2.size):
        return img1, img2

    # second case: an image can be contained in another
    img1_is_container = img1.size[0] > img2.size[0] and img1.size[1] > img2.size[1]
    img2_is_container = img2.size[0] > img1.size[0] and img2.size[1] > img1.size[1]
    if(img1_is_container):
        return dragImg(img1, img2)
    elif(img2_is_container):
        img2, img1 = dragImg(img2, img1)
        return img1, img2

    # third case: one dimension has the same value, but not the other
    if(img1.size[0] == img2.size[0] and img1.size[1] > img2.size[1]):
        # same length, img2 less height
        new_diff = img1.size[1] - img2.size[1]
        diff = round(new_diff/2)
        diff2 = diff if new_diff % 2 == 0 else diff-1
        if diff2 < 0 : diff2 = 0
        return img1, addTop(addBottom(img2, diff), diff2)
    if(img1.size[0] == img2.size[0] and img1.size[1] < img2.size[1]):
        # same length, img1 less height
        new_diff = img2.size[1] - img1.size[1]
        diff = round(new_diff/2)
        diff2 = diff if new_diff % 2 == 0 else diff-1
        if diff2 < 0 : diff2 = 0
        return addTop(addBottom(img1, diff), diff2), img2
    if(img1.size[0] > img2.size[0] and img1.size[1] == img2.size[1]):
        # same height, img2 less length
        new_diff = img1.size[0] - img2.size[0]
        diff = round(new_diff/2)
        diff2 = diff if new_diff % 2 == 0 else diff-1
        if diff2 < 0 : diff2 = 0
        return img1, addStart(addEnd(img2, diff), diff2)
    if(img1.size[0] < img2.size[0] and img1.size[1] == img2.size[1]):
        # same height, img1 less length
        new_diff = img2.size[0] - img1.size[0]
        diff = round(new_diff/2)
        diff2 = diff if new_diff % 2 == 0 else diff-1
        if diff2 < 0 : diff2 = 0
        return addTop(addBottom(img1, diff), diff2), img2

    # fourth case: lenght1 is bigger but height1 is smaller or viceversa
    if(img1.size[0] > img2.size[0] and img1.size[1] < img2.size[1]):
        diff_len = round((img1.size[0] - img2.size[0])/2)
        diff_high = round((img2.size[1] - img1.size[1])/2)
        diff_len2 = diff_len if diff_len%2==0 else diff_len-1
        diff_high2 = diff_high if diff_high%2==0 else diff_high-1
        return addTop(addBottom(img1, diff_high), diff_high2), addStart(addEnd(img2, diff_len), diff_len2)
    
    if(img1.size[0] < img2.size[0] and img1.size[1] > img2.size[1]):
        diff_len = round((img2.size[0] - img1.size[0])/2)
        diff_high = round((img1.size[1] - img2.size[1])/2)
        diff_len2 = diff_len if diff_len%2==0 else diff_len-1
        if(diff_len2 == -1):
            diff_len2 = 1
        diff_high2 = diff_high if diff_high%2==0 else diff_high-1
        if(diff_high2 == -1):
            diff_high2 = 1
        return addStart(addEnd(img1, diff_len), diff_len2), addTop(addBottom(img2, diff_high), diff_high2)

# drags the smaller image (content) until it has the same length or height as the container and them adds
# some rows or columns to result in two images with the same size
def dragImg(container, content):
    diff_len = container.size[0] - content.size[0]
    diff_hig = container.size[1] - content.size[1]

    rateo_cont = round(container.size[0]/content.size[0],5)
    rateo_tent = round(container.size[1]/content.size[1],5)
    # if they are proportional
    if(rateo_cont == rateo_tent):
        content = content.resize(container.size)
        return container, content

    if(content.size[0] < content.size[1]):
        if(diff_len ==1):
            return container, addStart(content, 1)  
        new_len = math.floor(content.size[0]*rateo_tent)
        content = content.resize((new_len, container.size[1]))
        new_diff_len = container.size[0] - content.size[0]
        diff = math.floor(new_diff_len/2)
        diff2 = diff if new_diff_len % 2 == 0 else diff+1
        return container, addStart(addEnd(content, diff), diff2)
    else:
        if(diff_hig ==1):
            return container, addBottom(content, 1)
        new_hig = math.floor(content.size[1]*rateo_cont)
        content = content.resize((container.size[0], new_hig))
        new_diff_hig = container.size[1] - content.size[1]
        diff = math.floor(new_diff_hig/2)
        diff2 = diff if new_diff_hig % 2 == 0 else diff+1
        return container, addTop(addBottom(content, diff), diff2)

# adds black columns at the start of the image
def addStart(image, cols):
    rows = image.size[1]
    columns_start = np.zeros((rows, cols, 3), dtype=np.uint8)
    res = np.column_stack([columns_start, np.array(image)])
    return Image.fromarray(res, 'RGB')

# adds black columns at the end of the image
def addEnd(image, cols):
    rows = image.size[1]
    columns_end = np.zeros((rows, cols, 3), dtype=np.uint8)
    res = np.column_stack([np.array(image), columns_end])
    return Image.fromarray(res, 'RGB')

# adds black rows at the top of the image
def addTop(image, rows):
    col = image.size[0]
    rows_top = np.zeros((rows, col, 3), dtype=np.uint8)
    res = np.row_stack([rows_top, np.array(image)])
    return Image.fromarray(res, 'RGB')

# adds black rows at the bottom of the image
def addBottom(image, rows):
    col = image.size[0]
    rows_bottom = np.zeros((rows, col, 3), dtype=np.uint8)
    res = np.row_stack([np.array(image), rows_bottom])
    return Image.fromarray(res, 'RGB')
