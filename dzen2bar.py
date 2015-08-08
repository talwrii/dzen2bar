"dzen2bar - version of i3bar that uses dzen2 for output and adds some features"

import argparse
import itertools
import json
import subprocess
import sys

def get_block_width(font, text):
    #  It looks like dzen2-textwidth doesn't support ttf while dzen2 does
    #     unicode characters are common enough that we need ttf fonts
    #     just drop support for min_width
    raise Exception('broken')
    # result = subprocess.check_output(['dzen2-textwidth', font, text])
    # return int(result)

def format_block(block, final=False, ignore_min_width=False, ignore_pango=False):
    dzen2_markup = block.get('dzen2_markup')
    text = block['full_text']
    color = block.get('color')
    separator = block.get('separator', True)
    min_width = block.get('min_width', None)
    #align = block.get('align', 'left')

    pixmap = block.get('dzen2_pixmap')

    if dzen2_markup:
        return dzen2_markup

    if min_width and not ignore_min_width:
        raise Exception('Min width not supported')

    if block.get('markup', 'none') != 'none' and not ignore_pango:
        raise Exception('Pango not supported')

    result = text
    if color:
        result = '^fg({})'.format(color) + result + '^fg()'

    if pixmap:
        result += '^i({})'.format(pixmap)

    if separator and not final:
            result += '|'
    return result


def calculate_padding(min_width, block_width, align):
    padding = max(0, min_width - block_width)
    if align == 'left':
        left_padding = 0
    elif align == 'right':
        left_padding = padding
    elif align == 'center':
        left_padding = padding // 2
    right_padding = padding - left_padding
    return left_padding, right_padding

def pad_string(min_width, align, string):
    block_width = get_block_width(args.font, string)
    left_padding, right_padding = calculate_padding(
        min_width, block_width, align)

    result = string
    if left_padding:
        result = 'p^({})'.format(left_padding) + result

    if right_padding:
        result = result + 'p^({})'.format(right_padding)
    return result

def parse_args():
    PARSER = argparse.ArgumentParser(description='Like i3bar but uses dzen2')

    # I can't find out how to work out what font we use by default
    #   we need to know the font to work out widths correctly
    PARSER.add_argument('font', type=str, help='Font to use')
    PARSER.add_argument('--screen', '-s', type=str, action='append',
        help='Font to use', default='1')
    PARSER.add_argument('--ignore-min-width', action='store_true',
        default=False,
        help='We cannot deal with min-width arguments. Silently ignore these')
    PARSER.add_argument('--ignore-pango', action='store_true', default=False,
        help='We cannot deal with pango markup. Ignore these tags')
    return PARSER.parse_args()

def main():
    args = parse_args()
    _version_line = sys.stdin.readline()
    _open_line = sys.stdin.readline()
    dzens = [subprocess.Popen(
        ['dzen2', '-xs', s, '-ta', 'right', '-fn', args.font],
        stdin=subprocess.PIPE)
             for s in args.screen]

    while True:
        line = sys.stdin.readline()
        line = line.strip(',')
        msg = json.loads(line)
        for dzen in dzens:
            rev_finalness = itertools.chain([True], itertools.repeat(False))
            result = ''
            for block, final in reversed(zip(reversed(msg), rev_finalness)):
                result += format_block(block, final=final,
                    ignore_min_width=args.ignore_min_width,
                    ignore_pango=args.ignore_pango)

            dzen.stdin.write(result.encode('utf8'))
            dzen.stdin.write('\n')
            dzen.stdin.flush()

if __name__ == '__main__':
	main()
