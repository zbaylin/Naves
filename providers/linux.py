from subprocess import check_output
import os
from xdg.DesktopEntry import DesktopEntry
from models.datum import Datum
from models.data_provider import DataProvider


class Linux(DataProvider):
  def __init__(self):
    super().__init__()
    self.name = "Linux"

  def run(self, term):
    data = []
    for file in os.listdir("/usr/share/applications"):
      if file.endswith(".desktop"):
        entry = DesktopEntry(os.path.join("/usr/share/applications", file))
        data.append(Datum(entry.getName(), entry.getComment()))

    return [datum for datum in data if term in datum.title]


main = Linux
