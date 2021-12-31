#
# Font Class
#

import requests


class Font:

    def __init__(self, family, weight, italic=0):
        self.family = family
        self.weight = weight
        self.italic = italic
        self.src = self._gen_url()
        self.valid = self._valid()
        self.name = self._gen_name()

    def _gen_url(self):
        if self.italic == 0:
            return f'{self.family.src}:wght@{self.weight}'
        else:
            return f'{self.family.src}:ital,wght@{self.italic},{self.weight}'

    def _valid(self):
        r = requests.get(self.src)
        if r.status_code == 200:
            return True
        return False

    def _gen_name(self):
        name = f'{self.family.name} {self.get_weight_name()}'

        if self.italic == 0:
            name = f'{name} Italic'

        return name

    def get_weight_name(self):
        if self.weight in self.family.weights:
            return self.family.weights.get(self.weight)
        else:
            return str(self.weight)
