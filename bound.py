from pt import Pt

class Bound:
  def __init__(self, min_x=float("inf"), max_x=float("-inf"), 
               min_y=float("inf"), max_y=float("inf")):
    self.min_x = min_x
    self.max_x = max_x
    self.min_y = min_y
    self.max_y = max_y
  
  def expand(self, pt: Pt):
    self.min_x = min(pt.x, self.min_x)
    self.max_x = max(pt.x, self.max_x)
    self.min_y = min(pt.y, self.min_y)
    self.max_y = max(pt.y, self.max_y)
    
  def is_within(self, pt: Pt):
    return self.min_x <= pt.x <= self.max_x and self.min_y <= pt.y <= self.max_y
  
  @property
  def len_x(self):
    return max(self.max_x - self.min_x, 0)
  
  @property
  def len_y(self):
    return max(self.max_y - self.min_y, 0)
  
  def combine_with(self, bound):
    self.min_x = min(self.min_x, bound.min_x)
    self.max_x = max(self.max_x, bound.max_x)
    self.min_y = min(self.min_y, bound.min_y)
    self.max_y = max(self.max_y, bound.max_y)