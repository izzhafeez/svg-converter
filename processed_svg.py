import geopandas as gpd

from bound import Bound
from feature import Feature
import re

class ProcessedSVG:
  def __init__(self, gdf: gpd.GeoDataFrame):
    self.gdf_records = gdf.to_dict("records")
    for gdf_dict in self.gdf_records:
      ProcessedSVG._add_details_to_dict(gdf_dict)
    self.features = [Feature(record, i) for i, record in enumerate(self.gdf_records)]
    bound = Bound()
    for feature in self.features:
      bound.combine_with(feature.bound)
       
  @staticmethod     
  def _add_details_to_dict(gdf_dict):
    description = gdf_dict["Description"]
    subzone, planning_area, region = ProcessedSVG._extract_details_from_description(description)
    gdf_dict["Subzone"] = subzone
    gdf_dict["Planning Area"] = planning_area
    gdf_dict["Region"] = region
    
  @staticmethod
  def _extract_details_from_description(description):
    _, subzone, _, _, planning_area, _, region, _, _, _ = re.findall("<td>(.*?)</td>", description)
    return (subzone, planning_area, region)
        
  def __str__(self):
    features_string = "".join([str(feat) for feat in self.features])
    xml_string = '<?xml version="1.0" encoding="utf-8" ?>'
    svg_string = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="650" width="800" id="svg2" class="jetpunk-svg">'
    style_string = '<style id="style1087">.border{stroke:#707070;stroke-width:0.5;stroke-opacity:1}.county{fill:#ffff80}</style>'
    return xml_string + svg_string + style_string + features_string + "</svg>"
        