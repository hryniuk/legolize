import argparse
import os.path

from PIL import Image, ImageStat, ImageDraw


def create_brick_circle(brick_size):
    white = (255,255,255,0)
    grey = (50, 50, 50, 100)
    cricle_brick_ratio = 0.4

    brick_circle = Image.new('RGBA', (brick_size, brick_size), white)

    brick_circle_context = ImageDraw.Draw(brick_circle)
    circle_size = int((cricle_brick_ratio * brick_size) / 2)
    brick_circle_context.ellipse(
            (circle_size, circle_size, brick_size-circle_size, brick_size-circle_size),
            outline=grey)

    return brick_circle


def legolize(input_file_path, output_file_path, *colors):
    try:
        img = Image.open(input_file_path)
    except FileNotFoundError:
        print(f"File {input_file_path} doesn't exist")

    if output_file_path is None:
        output_file_path = os.path.join(
                os.path.dirname(input_file_path),
                f"legolized-{os.path.basename(input_file_path)}")

    brick_size = 14
    brick_circle = create_brick_circle(brick_size)

    output_img = img.copy()
    for i in range(0, output_img.size[0], brick_size):
        for j in range(0, output_img.size[1], brick_size):
            cropped = output_img.crop((i, j, i + brick_size, j + brick_size))
            cropped = cropped.convert("RGBA")
            cropped_stats = ImageStat.Stat(cropped)
            cropped.paste(tuple(cropped_stats.median),
                    (0, 0, cropped.size[0], cropped.size[1]))
            cropped = Image.alpha_composite(cropped, brick_circle)
            output_img.paste(cropped, (i, j))

    output_img.save(output_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LEGOlize given image')
    parser.add_argument('-i', '--input-image', type=str,
                        help='image to legolize', required=True)
    parser.add_argument('-o', '--output-image', type=str, default=None,
                        help='output path')

    args = parser.parse_args()

    legolize(args.input_image, args.output_image)
