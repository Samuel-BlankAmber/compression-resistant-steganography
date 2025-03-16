import sys
from collections import Counter

from PIL import Image


def get_encoded_data(pixel):
    return "".join("1" if colour > 128 else "0" for colour in pixel)


def determine_colour_size(width, _height, pixel_data):
    first_row = pixel_data[:width]
    num_sames = []
    num_same = 1
    for pixel, prev_pixel in zip(first_row[1:], first_row):
        if get_encoded_data(pixel) == get_encoded_data(prev_pixel):
            num_same += 1
            continue
        num_sames.append(num_same)
        num_same = 1
    return Counter(num_sames).most_common(1)[0][0]


def decode_pixel_data(width, height, pixel_data):
    colour_size = determine_colour_size(width, height, pixel_data)

    encoded_data = ""
    for y in range(colour_size // 2, height, colour_size):
        for x in range(colour_size // 2, width, colour_size):
            pixel = pixel_data[y * width + x]
            encoded_data += get_encoded_data(pixel)

    message = ""
    for i in range(0, len(encoded_data), 8):
        byte = int(encoded_data[i:i + 8], 2)
        if byte == 0:
            break
        message += chr(byte)
    return message


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s <image_path>" % sys.argv[0])
        sys.exit(1)

    image_path = sys.argv[1]

    image = Image.open(image_path)
    pixel_data = list(image.getdata())

    width, height = image.size
    message = decode_pixel_data(width, height, pixel_data)
    print(f"Decoded message: {message}")
