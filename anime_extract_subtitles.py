import os.path as osp
import re
from glob import glob


def naruto_order_episodes(x):
    return float(re.findall("(\d+)", x)[0])


def extract_naruto():
    subtitles_dir = './naruto_subtitles'
    lines = []
    for i, file in enumerate(sorted(glob(osp.join(subtitles_dir, '*.ass')), key=naruto_order_episodes)):
        lines += file_to_lines(i, file)

    with open('naruto-subtitles-merged.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def extract_monogatari():
    subtitles_dir = './monogatari_subtitles'
    lines = []
    files_list = glob(osp.join(subtitles_dir, '**', '*.ass')) + glob(osp.join(subtitles_dir, '*.ass'))
    for i, file in enumerate(sorted(files_list)):
        lines += file_to_lines(i, file)

    with open('monogatari-subtitles-merged.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def file_to_lines(i, file):
    quote_start = '!Effect,'
    lines = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            # print(line)
            if line.startswith('Dialogue'):
                s = line.find(quote_start)
                skip_len = len(quote_start)
                if s == -1:
                    s = line.find('0,,')
                    skip_len = len('0,,')
                quote = line[s + skip_len:]
                quote = quote.replace('\n', ' ').replace(r'\N', ' ')
                quote = re.sub(r'\{\\.*?\}', '', quote)
                if quote.endswith(' '):
                    quote = quote[:-1]
                # conditioning for gpt-2 model
                quote = f'{i + 1}|{quote}'
                lines.append(quote)
    return lines


def main():
    # extract_naruto()
    extract_monogatari()


if __name__ == '__main__':
    main()
