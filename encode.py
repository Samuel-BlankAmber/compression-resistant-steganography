from math import ceil
import random
import sys

from PIL import Image

MAX_COMPRESSION_DELTA = 16
MESSAGE_END_MARKER = b"\x00"


def nearest_neighbour_upscale(pixel_data, width, height, scale):
    pixel_data_2d = [pixel_data[i:i + width // scale]
                     for i in range(0, len(pixel_data), width // scale)]

    new_pixel_data_2d = []
    for row in pixel_data_2d:
        new_row = []
        for pixel in row:
            new_row += [pixel] * scale
        if len(new_row) < width:
            new_row += [row[-1] for _ in range(width - len(new_row))]
        new_pixel_data_2d += [new_row] * scale
    if len(new_pixel_data_2d) < height:
        new_pixel_data_2d += [new_pixel_data_2d[-1]
                              for _ in range(height - len(new_pixel_data_2d))]

    new_pixel_data = [pixel for row in new_pixel_data_2d for pixel in row]
    return new_pixel_data


def rand_colour_channel():
    return random.randint(0, 255)


def message_to_pixels(message, bits_available):
    binary = "".join(f"{char:08b}" for char in message)
    colours = []
    for bit in binary:
        if bit == "0":
            colours.append(random.randint(0, 128 - MAX_COMPRESSION_DELTA))
        else:
            colours.append(random.randint(128 + MAX_COMPRESSION_DELTA, 255))
    colours += [rand_colour_channel()
                for _ in range(bits_available - len(colours))]
    assert len(colours) % 3 == 0
    return [(colours[i], colours[i + 1], colours[i + 2]) for i in range(0, len(colours), 3)]


if __name__ == "__main__":
    if len(sys.argv) != 5 and len(sys.argv) != 6:
        print("Usage: %s <width> <height> <message> <output_image> [colour_size]" %
              sys.argv[0])
        sys.exit(1)

    width = int(sys.argv[1])
    height = int(sys.argv[2])
    message = sys.argv[3].encode()
    output_image = sys.argv[4]
    colour_size = 1 if len(sys.argv) == 5 else int(sys.argv[5])

    message += MESSAGE_END_MARKER

    bits_available = (width // colour_size) * (height // colour_size) * 3
    bits_required = ceil(len(message) * 8 / 6) * 6
    if bits_required > bits_available:
        print(
            f"Message too long to encode in image. Need {bits_required} bits, but only have {bits_available} bits available.")
        sys.exit(1)

    pixel_data = message_to_pixels(message, bits_available)
    if colour_size > 1:
        pixel_data = nearest_neighbour_upscale(
            pixel_data, width, height, colour_size)
    image = Image.new("RGB", (width, height))
    image.putdata(pixel_data)
    image.save(output_image)
