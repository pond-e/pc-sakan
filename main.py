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
    if args[1] == '-i':
        output_color_r = args[2]
        output_color_g = args[3]
        output_color_b = args[4]
        input_file_name = args[5]
    else:
        input_file_name = args[1]
    
    background_img = cv2.imread(input_file_name)
    background_img_height = background_img.shape[0]
    background_img_width = background_img.shape[1]
    if background_img_height > background_img_width:
        output_width = int(background_img_height * (16/9))
        output_height = background_img_height
    else:
        output_width = background_img_width
        output_height = int(background_img_width * (9/16))

    if args[1] != '-i':
        (output_color_b, output_color_g, output_color_r) = most_used_color(background_img)

    padding_b = np.full((output_height, output_width), output_color_b)
    padding_g = np.full((output_height, output_width), output_color_g)
    padding_r = np.full((output_height, output_width), output_color_r)
    padding = np.stack([padding_b, padding_g, padding_r], 2)

    width_adjust = (output_width//2 + background_img_width//2) - (output_width//2 - background_img_width//2) - background_img_width
    # image synthesis
    padding[0:background_img_height, (output_width//2 - background_img_width//2):(output_width//2 + background_img_width//2 - width_adjust)] = background_img
    
    

    length_to_file_extension = len(input_file_name)
    while(input_file_name[length_to_file_extension - 1] != '.'):
        length_to_file_extension -= 1
    cv2.imwrite(input_file_name[:length_to_file_extension - 1]+'_desktop.png', padding)
    print("finish!")