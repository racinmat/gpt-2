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
    # todo: 58 is making mess, 100 too
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
    # todo: look at a histogram of durations, they are in miliseconds, and probably crop < 500ms? or 200?
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
        quote = line.text
        quote = quote.replace('\n', ' ').replace(r'\N', ' ')
        quote = re.sub(r'\{.*?\}', '', quote)
        if quote.endswith(' '):
            quote = quote[:-1]
        # conditioning for gpt-2 model
        if quote == '':
            continue
        quote = f'{i + 1}|{quote}'
        quote = re.sub('\s+', ' ', quote).strip()  # multiple whitespaces replaced by one
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
