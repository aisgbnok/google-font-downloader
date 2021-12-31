#
# Font Family Class
#

from src.font import Font


class Family:
    base_url = 'https://fonts.googleapis.com/css2?family='
    weights = {
        100: 'Thin',
        200: 'Extra Light',
        300: 'Light',
        400: 'Regular',
        500: 'Medium',
        600: 'SemiBold',
        700: 'Bold',
        800: 'Extra Bold',
        900: 'Black'
    }

    def __init__(self, name, find=True, fonts=None):
        if fonts is None:
            fonts = []

        self.name = name.strip()
        self.src = self.base_url + self.name.replace(' ', '+')
        self.fonts = fonts

        if find:
            self._find_all_fonts()

        print(self.name)
        print(self.src)

    def _find_all_fonts(self):
        valid_fonts = []

        for weight in range(100, 900 + 1, 100):
            normal_font = Font(self, weight)
            italic_font = Font(self, weight, 1)

            if normal_font.valid:
                valid_fonts.append(normal_font)

            if italic_font.valid:
                valid_fonts.append(italic_font)

        for font in valid_fonts:
            print(font.valid)

    def get_url(self, weight=None, italic=0):
        if weight is None:
            if italic == 0:
                return self.src
            else:
                return f'{self.src}:ital@{italic}'
        else:
            return Font(weight, italic).src

    def add_font(self, font):
        self.fonts.append(font)
