class DataProvider():
  def __init__(self, name):
    self.name = name
    self.results = []

  def run(self):
    raise NotImplementedError
