import numpy as np
import re
from shapely.geometry import MultiPolygon, Polygon
from shapely import wkt

from bound import Bound
from pt import Pt
from svg_format_converter import convert_path_absolute_to_relative
from utils import capitalize_words

class Feature:
  def __init__(self, details, index):
    self.geometry = Feature._convert_to_multipolygon(details["geometry"])
    
    self.details = details
    del self.details["geometry"]
    
    self.index = index
    
  @staticmethod
  def _convert_to_multipolygon(geometry):
    return MultiPolygon([geometry]) if isinstance(geometry, Polygon) else geometry
  
  def transform_geometry(self, bound):
    new_geometry = MultiPolygon([self.transform_polygon(g, bound) for g in self.geometry.geoms])
    path_datas = re.findall('d="(.*?)"', new_geometry.svg())
    self.svg_ds = [convert_path_absolute_to_relative(path_data) for path_data in path_datas]
    
  def transform_polygon(self, g, bound):
    scale_factor = max(bound.len_x, bound.len_y) / 800
    xys = g.exterior.coords.xy
    xs = (np.array(xys[0]) - bound.min_x) / scale_factor
    ys = (bound.max_y - np.array(xys[1])) / scale_factor
    new_polygon = Polygon(zip(xs, ys)).simplify(0.5)
    return wkt.loads(wkt.dumps(new_polygon, rounding_precision=5))
    
  def get_bound(self):
    bound = Bound()
    
    for g in self.geometry.geoms:
      for x, y in g.exterior.coords.xy:
        bound.expand(Pt(x, y))
      
    self.bound = bound
  
  def __str__(self, id_name, classes):
    id_ = self.details[id_name]
    id_ = capitalize_words(id_)
    combined_path = "".join(self.svg_ds)
    string = f'<path class="{classes}" id="{self.index+1}" d="{combined_path}"/>'
    return string