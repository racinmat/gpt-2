import os.path as osp
import re
from glob import glob

import pysubs2


def naruto_order_episodes(x):
    return float(re.findall("(\d+)", x)[0])


def extract_naruto():
    subtitles_dir = './naruto_subtitles'
    lines = []
    for i, file in enumerate(sorted(glob(osp.join(subtitles_dir, '*.ass')), key=naruto_order_episodes)):
        lines += file_to_lines_simple(i, file)

    with open('naruto-subtitles-merged.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def extract_monogatari():
    # todo: 44, 45, 61 is weird, 116
    subtitles_dir = './monogatari_subtitles'
    lines = []
    for i, file in enumerate(sorted(glob(osp.join(subtitles_dir, '**', '*.ass'), recursive=True))):
        lines += file_to_lines_complex(i, file)

    with open('monogatari-subtitles-merged.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def file_to_lines_simple(i, file):
    lines = []
    subs = pysubs2.load(file, encoding="utf-8")
    for line in subs:
        quote = line.text
        quote = quote.replace('\n', ' ').replace(r'\N', ' ')
        quote = re.sub(r'\{.*?\}', '', quote)
        if quote.endswith(' '):
            quote = quote[:-1]
        # conditioning for gpt-2 model
        quote = f'{i + 1}|{quote}'
        quote = re.sub('\s+', ' ', quote).strip()  # multiple whitespaces replaced by one
        if quote == '':
            continue
        lines.append(quote)
    return lines


def file_to_lines_complex(i, file):
    lines = []
    prev_quote = None
    subs = pysubs2.load(file, encoding="utf-8")
    import numpy as np
    import matplotlib.pyplot as plt
    durs = []
    for line in subs:
        durs.append(line.duration)
        if line.duration < 200:
            continue
        if line.style == 'Black and Red':   # empirically found this style contains weird texts
            continue
        quote = line.text
        quote = quote.replace('\n', ' ').replace(r'\N', ' ').replace(r'\h', ' ')
        quote = re.sub(r'\{.*?\}', '', quote)
        if re.match('^m -?\d+(\.\d+)? -?\d+(\.\d+)?', quote): # those weird long numeric sequences
            continue
        if quote.endswith(' '):
            quote = quote[:-1]
        # conditioning for gpt-2 model
        if quote == '':
            continue
        quote = re.sub('\s+', ' ', quote).strip()  # multiple whitespaces replaced by one
        quote = f'{i + 1}|{quote}'
        if prev_quote != quote:
            lines.append(quote)
        prev_quote = quote

    np_durs = np.array(durs)
    y = np.bincount(np_durs)
    ii = np.nonzero(y)[0]
    histogram = np.array(list(zip(ii, y[ii])))
    return lines


def main():
    # extract_naruto()
    extract_monogatari()


if __name__ == '__main__':
    main()
