import os
import string
from pathlib import Path

import requests

from src.font_family import Family

directory = './fonts'

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


class Font:
    def __init__(self, family, style, weight, src):
        self.name = None
        self.family = family
        self.style = style
        self.weight = int(weight)
        self.variant_name = None
        self.src = src
        self.format = self.gen_format()
        self.filename = None
        self.version = self.gen_version()

        self.gen_names()

    def gen_format(self):
        period_index = self.src.rfind('.')

        return self.src[period_index + 1:]

    def gen_version(self):
        start_v = '/v'
        end_v = '/'

        start = self.src.find(start_v) + len(start_v)
        version = self.src[start:]

        end = version.find(end_v)
        version = version[:end]

        return version

    def gen_names(self):
        family_name = self.family
        weight_name = self.get_weight_name()

        name = family_name + " " + weight_name
        filename = family_name.replace(' ', '') + "-" + weight_name
        variant_name = weight_name

        if self.style != 'normal':
            style_name = self.style.capitalize()

            name += " " + style_name
            variant_name += " " + style_name
            filename += style_name

        self.name = name
        self.filename = filename
        self.variant_name = variant_name

    def get_weight_name(self):
        if self.weight in weights:
            return weights.get(self.weight)
        else:
            return str(self.weight)

    def get_ext(self):
        return '.' + self.format


def get_line(text, line_index):
    line = text
    end_char = '\n'

    # Remove all lines before line_index
    for i in range(line_index):
        end = line.find(end_char)
        line = line[end:]

    # Find end of that line
    end = line.find(end_char)

    # Return line at line_index
    return line[:end].strip()


def remove_line(text):
    end_char = '\n'

    end = text.find(end_char) + 1
    return text[end:]


def find_font_block(text, start_index):
    start_text = '@font-face {'
    end_text = '}'

    start_block = text.find(start_text, start_index) + len(start_text)
    end_block = text.find(end_text, start_index)

    return [start_block, end_block]


def get_font_block(text, start_index, end_index):
    return text[start_index: end_index].strip('\n')


def get_line_value(line):
    start = line.find(':') + 1
    end = line.find(';')

    value = line[start:end].strip()
    if value[0] == '\'':
        value = value.translate(str.maketrans('', '', string.punctuation))
    elif value[:3] == 'url':
        value = value[4:value.find(')')]

    return value


def parse_font_block(text):
    line = get_line(text, 0)
    text = remove_line(text)

    # Font Family
    family_value = get_line_value(line)
    line = get_line(text, 0)
    text = remove_line(text)

    # Font Style
    style_value = get_line_value(line)
    line = get_line(text, 0)
    text = remove_line(text)

    # Font Weight
    weight_value = get_line_value(line)

    # src
    line = text
    src_value = get_line_value(line)

    return Font(family_value, style_value, weight_value, src_value)


def save_font(font):
    print(f'{font.name}')
    url = font.src

    print(f'{font.src}')
    response = requests.get(url)

    rel_dir = Path(f'{directory}/{font.family}/{font.format}')
    rel_filename = Path(f'{font.filename}{font.get_ext()}')
    path = Path(f'{rel_dir}/{rel_filename}')

    rel_dir.mkdir(parents=True, exist_ok=True)
    print(f'{path}\n')

    with open(path, 'wb') as file:
        file.write(response.content)


def process_url(url):
    # Save css file
    response = requests.get(url)
    file = response.text

    index = 0
    fonts = []

    while index + 1 < len(file):
        char_index = find_font_block(file, index)
        text = get_font_block(file, char_index[0], char_index[1])

        font = parse_font_block(text)
        fonts.append(font)

        index = char_index[1] + 1

    rel_dir = Path(f'{directory}/{fonts[0].family}/{fonts[0].format}')
    rel_filename = Path(f'')

    for font in fonts:
        save_font(font)


def process_urls(urls):
    for url in urls:
        process_url(url)


def main():
    # Fonts to download
    urls = [

    ]

    # Process all urls
    process_urls(urls)


if __name__ == '__main__':
    main()
