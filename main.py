import cv2
import numpy as np
import sys
import statistics
import time


def most_used_color(img):
    # https://zenn.dev/kazaki/articles/4bc99a27e33d24
    color_arr = np.vstack(img)
    color_code = ['{:02x}{:02x}{:02x}'.format(*color) for color in color_arr]

    mode = statistics.mode(color_code)
    b = int(mode[0:2], 16)
    g = int(mode[2:4], 16)
    r = int(mode[4:6], 16)
    color_mode = (b, g, r)
    return color_mode


if __name__ == '__main__':
    args = sys.argv
    
    background_img = cv2.imread(args[1])
    background_img_height = background_img.shape[0]
    background_img_width = background_img.shape[1]
    output_width = int(background_img_height * (16/9))
    output_height = background_img_height

    (b, g, r) = most_used_color(background_img)

    padding_b = np.full((output_height, output_width), b)
    padding_g = np.full((output_height, output_width), g)
    padding_r = np.full((output_height, output_width), r)
    padding = np.stack([padding_b, padding_g, padding_r], 2)

    width_adjust = (output_width//2 + background_img_width//2) - (output_width//2 - background_img_width//2) - background_img_width
    # image synthesis
    padding[0:background_img_height, (output_width//2 - background_img_width//2):(output_width//2 + background_img_width//2 - width_adjust)] = background_img
    
    length_to_file_extension = len(args[1])
    while(args[1][length_to_file_extension - 1] != '.'):
        length_to_file_extension -= 1
    cv2.imwrite(args[1][:length_to_file_extension - 1]+'_desktop.png', padding)