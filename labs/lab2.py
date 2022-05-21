#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image



# COLOR FILTER FROM GREYSCALE FILTER

def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_filter(image):
        rgb = split_color(image)

        # print(image['height'])
        # print(image['width'])
        # print(len(image['pixels']))
        # print(rgb[0]['height'])
        # print(rgb[0]['width'])
        # for i in range(3):
        #     print(len(rgb[i]['pixels']))
        
        comb_im = []
        for i in range(3):
            comb_im.append(filt(rgb[i]))
        r = combine_rgb(comb_im)
        return r
    return color_filter


# Helper Functions for Split Color Image and Combine Greyscale Images

def split_color(image):
    """
    Given a color image and produces a list of three greyscale images in RGB.
    """
    return [{
        'height': image['height'],
        'width': image['width'],
        'pixels': [image['pixels'][j][i] for j in range(len(image['pixels']))]
    } for i in range(3)]

def combine_rgb(rgb_images):
    """
    Given a list of three greyscale images in RGB and produces a color image.
    """
    return {
        'height': rgb_images[0]['height'],
        'width': rgb_images[0]['width'],
        'pixels': [(
            rgb_images[0]['pixels'][i],
            rgb_images[1]['pixels'][i],
            rgb_images[2]['pixels'][i]
        ) for i in range(len(rgb_images[0]['pixels']))]
    }
    # return {
    #     'height': rgb_images[0]['height'],
    #     'width': rgb_images[0]['width'],
    #     'pixels': [(rgb_images[j]['pixels'][i] for j in range(3)) for i in range(len(rgb_images[0]['pixels']))]
    # }

# VARIOUS FILTERS

def make_blur_filter(n):
    def blurred_for_color(image):
        return blurred(image, n)
    return blurred_for_color


def make_sharpen_filter(n):
    def sharpened_for_color(image):
        return sharpened(image, n)
    return sharpened_for_color


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def filters_comb(image):
        output = image.copy()
        for filter in filters:
            output = filter(output)
        return output
    return filters_comb


# SEAM CARVING

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """
    functions = filter_cascade(
        [greyscale_image_from_color_image, compute_energy, cumulative_energy_map, minimum_energy_seam]
    )
    output = image.copy()
    for i in range(ncols):
        seam = functions(output)
        output = image_without_seam(output, seam)
        print('step:', i)
    return output


# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    return {
        'height': image['height'],
        'width': image['width'],
        'pixels': [round(
            image['pixels'][i][0]*0.299 + 
            image['pixels'][i][1]*0.587 +
            image['pixels'][i][2]*0.114
        ) for i in range(len(image['pixels']))]
    }

def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    # print('grey: ', grey)
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    # print('energy: ', energy)
    width = energy['width']
    height = energy['height']
    pixels = energy['pixels']

    cumulative_energy_value = []

    for i in range(height):
        for j in range(width):
            index = i * width + j
            if i == 0:
                cumulative_energy_value.append(pixels[index])
            elif j == 0:
                cumulative_energy_value.append(
                    pixels[index] + 
                    min(
                        cumulative_energy_value[index - width],
                        cumulative_energy_value[index - width + 1]
                    )
                )
            elif j == width - 1:
                cumulative_energy_value.append(
                    pixels[index] + 
                    min(
                        cumulative_energy_value[index - width - 1],
                        cumulative_energy_value[index - width]
                    )
                )
            else:
                cumulative_energy_value.append(
                    pixels[index] + 
                    min(
                        cumulative_energy_value[index - width - 1],
                        cumulative_energy_value[index - width],
                        cumulative_energy_value[index - width + 1]
                    )
                )
            # print(len(cumulative_energy_value))
    return {
    'height': energy['height'],
    'width': energy['width'],
    'pixels': cumulative_energy_value
}


    # def cumulative_energy_per_pixel(pixel_num):
    #     if pixel_num < width:
    #         return pixels[pixel_num]
    #     elif pixel_num % width == 0:
    #         return (
    #             pixels[pixel_num] +
    #             min(cumulative_energy_per_pixel(pixel_num - width + i) for i in range(2))
    #         )
    #     elif pixel_num % width == width - 1:
    #         return (
    #             pixels[pixel_num] +
    #             min(cumulative_energy_per_pixel(pixel_num - width + i) for i in range(-1, 1))
    #         )
    #     else:
    #         return (
    #             pixels[pixel_num] +
    #             min(cumulative_energy_per_pixel(pixel_num - width + i) for i in range(-1, 2))
    #         )
    
    # return {
    #     'height': energy['height'],
    #     'width': energy['width'],
    #     'pixels': [cumulative_energy_per_pixel(i) for i in range(len(pixels))]
    # }

def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    # print('cem: ', cem)
    width = cem['width']
    height = cem['height']
    pixels = cem['pixels']
    # print('[31, 23, 15, 6]:', [pixels[i] for i in [31, 23, 15, 6]])
    # print('[2, 11, 21, 31]:', [pixels[i] for i in [2, 11, 21, 31]])

    seam = []

    # row = height - 1

    # while row >= 0:
    #     base_index = width * row
    #     if row == height - 1:
    #         pixels_consider = [pixels[i] for i in range(base_index, base_index + width)]
    #         seam.append(pixels_consider.index(min()))

    for i in range(height):
        row = height - 1 - i
        # print('rwo:', row)
        base_index = width * row
        if row == height - 1:
            energy = pixels[base_index]
            # print('energy:', energy)
            for column in range(width):
                if pixels[base_index + column] <= energy:
                    energy = pixels[base_index + column]
                    # print('energy:', energy)
                    index = base_index + column
            seam.append(index)
        else:
            # print('i:', i)
            # print('seam:', seam)
            seam_below = seam[i - 1]
            # print('seam_below:', seam_below)
            if seam_below % width == 0:
                for j in range(seam_below-width, seam_below-width+2):
                    if pixels[j] <= energy:
                        energy = pixels[j]
                        # print('energy:', energy)
                        index = j
                seam.append(index)
            elif seam_below % width == width - 1:
                for k in range(seam_below-width-1, seam_below-width+1):
                    if pixels[k] <= energy:
                        energy = pixels[k]
                        # print('energy:', energy)
                        index = k
                seam.append(index)
            else:
                for h in range(seam_below-width-1, seam_below-width+2):
                    if pixels[h] <= energy:
                        energy = pixels[h]
                        # print('energy:', energy)
                        index = h
                seam.append(index)     

    return seam

    # pixels_with_index = []

    # for i in range(width*height):
    #     pixels_with_index.append((pixels[i], i))

    # def find_min_per_row(row_num):
    #     if row_num == height - 1:
    #         return min(pixels_with_index[i] for i in range(width * (height - 1), width * height))
    #     elif find_min_per_row(row_num+1)

def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    # print(seam)

    return {
        'height': image['height'],
        'width': image['width'] - 1,
        'pixels': [image['pixels'][i] for i in range(image['height'] * image['width']) if i not in seam]
    }


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}

def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
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

def save_greyscale_image(image, filename, mode='PNG'):
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


# GREYSCALE HELPER FUNCTIONS/PARAMETERS

def get_pixel(image, x, y):
    if x < 0: x = 0
    elif x >= image['height']: x = image['height'] - 1    
    if y < 0: y = 0
    elif y >= image['width']: y = image['width'] - 1

    return image['pixels'][x * image['width'] + y]

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
    return result

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

# GREYSCALE FILTERS

def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
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


# MAIN

if __name__ == '__main__':

    # i_inv = load_color_image('test_images/cat.png')
    # save_color_image(color_filter_from_greyscale_filter(inverted)(i_inv), 'inverted.png')

    # i_blurred = load_color_image('test_images/python.png')
    # save_color_image(color_filter_from_greyscale_filter(make_blur_filter(9))(i_blurred), 'blurred.png')

    # i_sharpened = load_color_image('test_images/sparrowchick.png')
    # save_color_image(color_filter_from_greyscale_filter(make_sharpen_filter(7))(i_sharpened), 'sharpened.png')

    # filter1 = color_filter_from_greyscale_filter(edges)
    # filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
    # filt = filter_cascade([filter1, filter1, filter2, filter1])
    # i_cascade = load_color_image('test_images/frog.png')
    # save_color_image(filt(i_cascade), 'cascade.png')

    i_seam = load_color_image('test_images/construct.png')
    save_color_image(seam_carving(i_seam, 100), 'seam_carving_construct.png')

    pass
