class DataProvider():
  def __init__(self):
    self.name = ""
    self.results = []

  def run(self, term):
    raise NotImplementedError
