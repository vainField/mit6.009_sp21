#!/usr/bin/env python3

import math

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, x, y):
    if x < 0: x = 0
    elif x >= image['height']: x = image['height'] - 1    
    if y < 0: y = 0
    elif y >= image['width']: y = image['width'] - 1

    return image['pixels'][x * image['width'] + y]

# x * image['width'] + y

def set_pixel(image, x, y, c):
    image['pixels'][x * image['width'] + y] = c


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0] * (image['height'] * image['width']),
    }
    for x in range(image['height']):
        for y in range(image['width']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    # print(image)
    # print(result)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)


# HELPER FUNCTIONS

def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    Kernal is a dictionary with a matrix dimension and a list of numbers in 
    row-major order
    """
    assert kernel['dim'] % 2 == 1, 'dimension of kernel should be odd'
    assert round(len(kernel['num'])**0.5) == kernel['dim'], 'invalid kernal'
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0] * (image['height'] * image['width']),
    }
    offset = (kernel['dim']-1)//2

    for x in range(image['height']):
        for y in range(image['width']):
            row = x-offset
            column = y-offset
            color = 0
            for i in range(kernel['dim']):
                for j in range(kernel['dim']):
                    color += get_pixel(image, row+i, column+j) * kernel['num'][i*kernel['dim']+j]
            set_pixel(result, x, y, color)
    
    return result


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    return {
        'height': image['height'],
        'width': image['width'],
        'pixels': [round(i) if i <= 255 and i >= 0 else 255 if i > 255 else 0 for i in image['pixels']]
    }


def kernel_bblurred(dimension):
    return {'dim': dimension, 'num': [1/(dimension**2)] * (dimension**2)}

def kernel_shapened(dimension):
    k = {'dim': dimension, 'num': [-1/(dimension**2)] * (dimension**2)}
    k['num'][(dimension**2-1)//2] += 2
    return k

k_x = {'dim': 3, 'num': [
    -1, 0, 1,
    -2, 0, 2,
    -1, 0, 1
]}

k_y = {'dim': 3, 'num': [
    -1, -2, -1,
     0,  0,  0,
     1,  2,  1
]}

# FILTERS

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    # raise NotImplementedError

    # then compute the correlation of the input image with that kernel
    # raise NotImplementedError
    
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    # raise NotImplementedError
    return round_and_clip_image(correlate(image, kernel_bblurred(n)))


def sharpened(image, n):
    """
    Return a new image representing the result of applying a sharpening (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    return round_and_clip_image(correlate(image, kernel_shapened(n)))

def edges(image):
    """
    Return a new image representing the result of applying the Sobel operator
    to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """    
    x = correlate(image, k_x)
    y = correlate(image, k_y)

    return round_and_clip_image({
        'height': x['height'],
        'width': x['width'],
        'pixels': [round((x['pixels'][i]**2 + y['pixels'][i]**2)**0.5) for i in range(len(x['pixels']))]
    })



# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


# TEST FUNCTIONS

def compare_images(im1, im2):
    assert set(im1.keys()) == {'height', 'width', 'pixels'}, 'Incorrect keys in dictionary'
    assert im1['height'] == im2['height'], 'Heights must match'
    assert im1['width'] == im2['width'], 'Widths must match'
    assert len(im1['pixels']) == im1['height']*im1['width'], 'Incorrect number of pixels'
    assert all(isinstance(i, int) for i in im1['pixels']), 'Pixels must all be integers'
    assert all(0<=i<=255 for i in im1['pixels']), 'Pixels must all be in the range from [0, 255]'
    pix_incorrect = (None, None)
    for ix, (i, j) in enumerate(zip(im1['pixels'], im2['pixels'])):
        if i != j:
            pix_incorrect = (ix, abs(i-j))
    assert pix_incorrect == (None, None), 'Pixels must match.  Incorrect value at location %s (differs from expected by %s)' % pix_incorrect

# def test_inverted_2():
#     im = {
#         'height': 1,
#         'width': 4,
#         'pixels': [2, 90, 141, 218]
#     }
#     result = inverted(im)
#     expected = {
#         'height': 1,
#         'width': 4,
#         'pixels': [253, 165, 114, 37]
#     }
#     compare_images(result, expected)

def test_blurred_black_image():
    im = {
        'height': 6,
        'width': 5,
        'pixels': [0]*30
    }
    result = blurred(im, 3)
    expected = {
        'height': 6,
        'width': 5,
        'pixels': [0]*30
    }
    compare_images(result, expected)
    result = blurred(im, 5)
    compare_images(result, expected)

# def test_blurred_centered_pixel()
#     im = load_image('test_images/centered_pixel.png')
#     result = blurred(im, 3)


# MAIN

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.

    # test_inverted_2()
    # test_blurred_black_image()

    # i_inv = load_image('test_images/bluegill.png')
    # save_image(inverted(i_inv), 'inverted.png')

    # kernel_id = {'dim': 3, 'num': [
    #     0,0,0,
    #     0,1,0,
    #     0,0,0
    # ]}
    # kernel_tr = {'dim': 5, 'num': [
    #     0,0,0,0,0,
    #     0,0,0,0,0,
    #     1,0,0,0,0,
    #     0,0,0,0,0,
    #     0,0,0,0,0,
    # ]}
    # kernel_av = {'dim': 3, 'num': [
    #     0.0,0.2,0.0,
    #     0.2,0.2,0.2,
    #     0.0,0.2,0.0
    # ]}
    # kernel_fin = {'dim': 9, 'num': [
    #     0,0,0,0,0,0,0,0,0,
    #     0,0,0,0,0,0,0,0,0,
    #     1,0,0,0,0,0,0,0,0,
    #     0,0,0,0,0,0,0,0,0,
    #     0,0,0,0,0,0,0,0,0,
    #     0,0,0,0,0,0,0,0,0,
    #     0,0,0,0,0,0,0,0,0,
    #     0,0,0,0,0,0,0,0,0,
    #     0,0,0,0,0,0,0,0,0,
    # ]}

    # i_cor = load_image('test_images/construct.png')
    # save_image(correlate(i_cor, k_y), 'edge_y.png')

    # i_blurred = load_image('test_images/cat.png')
    # save_image(blurred(i_blurred, 5), 'blurred.png')

    # i_sharpened = load_image('test_images/python.png')
    # save_image(sharpened(i_sharpened, 11), 'sharpened.png')

    # i_edges = load_image('test_images/construct.png')
    # save_image(edges(i_edges), 'edges.png')

    pass




