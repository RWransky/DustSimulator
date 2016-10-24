import sys
import math
import cv2
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
from voronoi import *
from polygon_helpers import *
from plot_helpers import *
from landscape_helpers import tesselate_points
from forage_helpers import dust_drift

# constants used to create landscape
NUM_LANDSCAPES = 1
FIELD_LENGTH = 4000
HIVE_CENTER_X = FIELD_LENGTH/2
HIVE_CENTER_Y = FIELD_LENGTH/2
NUM_FIELDS = 15
# MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 100
PERCENT_WEEDY = 0


def SaveFigureAsImage(fileName, fig=None, **kwargs):
    ''' Save a Matplotlib figure as an image without borders or frames.
       Args:
            fileName (str): String that ends in .png etc.

            fig (Matplotlib figure instance): figure you want to save as the image
        Keyword Args:
            orig_size (tuple): width, height of the original image used to maintain
            aspect ratio.
    '''
    fig_size = fig.get_size_inches()
    w, h = fig_size[0], fig_size[1]
    fig.patch.set_alpha(0)
    # Aspect ratio scaling if required
    if 'orig_size' in kwargs:
        w, h = kwargs['orig_size']
        w2, h2 = fig_size[0], fig_size[1]
        fig.set_size_inches([(w2/w)*w, (w2/w)*h])
        fig.set_dpi((w2/w)*fig.get_dpi())
    a = fig.gca()
    a.set_frame_on(False)
    a.set_xticks([])
    a.set_yticks([])
    plt.axis('off')
    plt.xlim(0, h)
    plt.ylim(w, 0)
    fig.savefig(fileName, transparent=True, bbox_inches='tight', pad_inches=0)


def SaveFullSizeImg(fileName, field_length):
    img = cv2.imread(fileName)
    fx = field_length/float(img.shape[1])
    fy = field_length/float(img.shape[0])
    cv2.imwrite(fileName, cv2.resize(img, (0, 0), fx=fx, fy=fy))


def to_binary(img, lower_thresh, upper_thres):
    ret, thresh = cv2.threshold(img, lower_thresh, upper_thres, 0)
    return thresh


def to_zero_one(img, additive):
    img_max = np.max(img)
    img /= img_max
    return np.copy(img)*additive


def expand_margins(fileName, margin_width):
    image = cv2.imread(fileName)
    image2 = cv2.imread(fileName)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img, 0, 20)
    kernel = np.ones((3, 3), np.uint8)
    margins = cv2.dilate(edges, kernel, iterations=margin_width/3)

    not_corn_pre = to_binary(img2, 70, 80)
    corn = to_binary(img, 100, 140)

    not_corn = to_zero_one(not_corn_pre, 2) - to_zero_one(corn, 1)

    with_margin = not_corn + to_zero_one(margins, 3)

    return with_margin


def group_points(x, percent_weedy):
    corn_pts = np.argwhere(x == 1)
    soy_pts = np.argwhere(x == 2)
    margin_pts = np.argwhere(x > 2)

    if percent_weedy == 0:
        return corn_pts, margin_pts
    elif percent_weedy < 100:
        numer, denom = (percent_weedy).as_integer_ratio()
        weeds = np.array_split(soy_pts, denom)
        weed_arr = weeds[0]
        for i in range(numer-1):
            weed_arr = np.concatenate((weed_arr, weeds[i]), axis=0)
        print weed_arr.shape, margin_pts.shape
        return corn_pts, np.concatenate((weed_arr, margin_pts), axis=0)
    else:
        return corn_pts, np.concatenate((soy_pts, margin_pts), axis=0)


def contaminate(flower, corn):
    ll = np.array([flower[0]-100, flower[1]-100])  # lower-left
    ur = np.array([flower[0]+100, flower[1]+100])  # upper-right

    inidx = np.all(np.logical_and(ll <= corn, corn <= ur), axis=1)
    if corn[inidx].shape[0] == 0:
        return 0
    else:
        dist = distance.cdist(corn[inidx], np.reshape(flower, (1, 2)), 'euclidean')
        lowest_dist = np.min(dist)
        return dust_drift(lowest_dist)


def generate_margin(field_length, num_fields, percent_weedy, margin_width, num):
    area, regions, vertices, points = tesselate_points(field_length, num_fields)

    order = np.arange(num_fields)
    np.random.shuffle(order)

    num_corn = np.uint32(num_fields*0.4)

    num_weedy_corn = np.uint32(num_corn*percent_weedy)

    if num_weedy_corn == 0:
        if percent_weedy > 0:
            num_weedy_corn = 1

    num_weedy_soy = np.uint32((num_fields-num_corn)*.45)

    marker = []
    # for marker 0=soy no weeds 1=soy weeds 2=corn no weeds 3=corn weeds
    for i in range(0, num_corn):
        if i < num_weedy_corn:
            marker.append(3)
        else:
            marker.append(2)
    for j in range(0, (num_fields-num_corn)):
        if j < num_weedy_soy:
            marker.append(1)
        else:
            marker.append(0)

    plt.figure(1)

    for index in range(num_fields):
        is_corn = False
        is_soy = False
        if marker[index] > 1:
            is_corn = True
        else:
            is_soy = True

        region = regions[order[index]]
        polygon = format_polygon(vertices[region], field_length)
        centroid = points[order[index]]

        if is_corn:
            plt.fill(*zip(*polygon), facecolor='y')
        else:
            plt.fill(*zip(*polygon), facecolor='g')

    SaveFigureAsImage('landscape'+str(num), plt.figure(1), orig_size=(field_length, field_length))
    SaveFullSizeImg('landscape'+str(num)+'.png', field_length)
    return expand_margins('landscape'+str(num)+'.png', MARGIN_WIDTH)


def create_fields(field_length, num_fields, percent_weedy, margin_width, num):
    landscape = generate_margin(field_length, num_fields, percent_weedy, margin_width, num)
    corn, flowers = group_points(landscape, percent_weedy)
    return corn, flowers
