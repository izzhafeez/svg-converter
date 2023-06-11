import re

def convert_path_absolute_to_relative(absolute_path, decimal_places=5):
  xy_pairs = re.findall("(\d+\.\d+),(\d+\.\d+)", absolute_path)
  curr_x = 0
  curr_y = 0
  new_xy_pairs = []
  for x, y in xy_pairs:
    new_x = round(float(x) - curr_x, decimal_places)
    new_y = round(float(y) - curr_y, decimal_places)
    new_xy_pair: str = f"{new_x} {new_y}"
    new_xy_pairs.append(new_xy_pair)
    curr_x = float(x)
    curr_y = float(y)
    
  new_path = "M" + "l".join(new_xy_pairs) + "z"
  return new_path.replace(",", " ")
