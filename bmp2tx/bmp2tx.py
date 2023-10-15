import os
import sys
import argparse

from PIL import Image

def convert(screen_width, src_image_dir):

  # frame index offset (fix)
  frame_index_offset = 10000

  # frame number
  n = 0

  bmp_files = sorted(os.listdir(src_image_dir))

  for i,bmp_name in enumerate(bmp_files):

    if bmp_name.endswith(".bmp"):

      print(bmp_name)
            
      im = Image.open(src_image_dir + "/" + bmp_name)

      im_width, im_height = im.size
      if im_width != screen_width:
        print("error: image width is not same as screen width.")
        break

      im_bytes = im.tobytes()

      grm_bytes = bytearray(screen_width * im_height * 2)
      for y in range(im_height):
        for x in range(im_width):
          r = im_bytes[ (y * im_width + x) * 3 + 0 ]
          g = im_bytes[ (y * im_width + x) * 3 + 1 ]
          b = im_bytes[ (y * im_width + x) * 3 + 2 ]
          r >>= 3
          g >>= 3
          b >>= 3
          c = (g << 11) | (r << 6) | (b << 1)
          if c > 0:
            c += 1
          grm_bytes[ y * 256 * 2 + x * 2 + 0 ] = c // 256
          grm_bytes[ y * 256 * 2 + x * 2 + 1 ] = c % 256

      frame_index = n + frame_index_offset
      frame_group = n // 500

      grm_file_name = f"im{frame_group:02d}/Tx{frame_index:05d}"

      os.makedirs(f"im{frame_group:02d}", exist_ok=True)

      with open(grm_file_name, "wb") as f:
        f.write(grm_bytes)

#      print(".", end="", flush=True)

      n += 1


# main
def main():

  parser = argparse.ArgumentParser()

#  parser.add_argument("screen_width", help="output screen width (256,384,512)", type=int)
  parser.add_argument("src_image_dir", help="source individual image directory")
#  parser.add_argument("output_file", help="output file name")

  args = parser.parse_args()

  convert(256, args.src_image_dir)


if __name__ == "__main__":
    main()
