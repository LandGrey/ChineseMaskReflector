#!/usr/bin/env python
# coding: utf-8
# Build By LandGrey


import io
import os
import re
import sys
import time
import argparse
from pypinyin import lazy_pinyin


def parse_operator(content_list, pattern):
    """
    :param content_list: ['wang', 'hong', 'mei']
    :param pattern: [['2', 'lower', 'default'], ['3', 'lower', 'default'], ['0', 'append', '@'], ['1', 'upper', '=1']]
    :return:
    """
    result_list = ['' for _ in range(len(pattern))]
    pattern_count = 0
    for p in pattern:
        position = p[0]
        operator = p[1]
        ranges = p[2]
        if operator == 'append':
            result_list[pattern_count] = ranges
            pattern_count += 1
            continue
        if position == 'default':
            if pattern_count < len(content_list):
                content = content_list[pattern_count]
            else:
                continue
        elif int(position) > 0 and len(content_list) > (int(position) - 1):
            content = content_list[int(position)-1]
        else:
            continue
        content = content.replace('%|%', ',').replace('%-%', ':')
        if ranges == 'default':
            result_list[pattern_count] = content
        elif not ranges[-1].isdigit():
            result_list[pattern_count] = ranges
        else:
            ranges_op = ranges[:len(ranges) - 1]
            if ranges_op == '=' or ranges_op == '==':
                result_list[pattern_count] = content[int(ranges[-1])-1:int(ranges[-1])]
            elif ranges_op == '>':
                result_list[pattern_count] = content[int(ranges[-1]):]
            elif ranges_op == '>=':
                result_list[pattern_count] = content[int(ranges[-1])-1:]
            elif ranges_op == '<':
                result_list[pattern_count] = content[:int(ranges[-1])-1]
            elif ranges_op == '<=':
                result_list[pattern_count] = content[:int(ranges[-1])]
            else:
                continue
        if operator == 'default' or operator == 'lower':
            result_list[pattern_count] = str(result_list[pattern_count]).lower()
        elif operator == 'upper':
            result_list[pattern_count] = str(result_list[pattern_count]).upper()
        elif operator == 'reverse':
            result_list[pattern_count] = str(result_list[pattern_count])[::-1]
        elif operator == 'remove':
            result_list[pattern_count] = ''
        elif operator == 'append':
            result_list[pattern_count] = ranges
        pattern_count += 1
    return ''.join(result_list)


def prepare_pattern(pattern):
    result = []
    for p in pattern.split(','):
        matches = re.findall('\{(.*?):(.*?):(.*?)\}+', p, re.I | re.M | re.S)
        elements = []
        for match in matches:
            ele = []
            if len(match) == 3:
                position = match[0].strip()
                operator = match[1].strip()
                ranges = match[2].strip()
                if position and position != 'default' and not str(position).isdigit():
                    exit('[-] position: [{}] is invalid'.format(position))
                if operator and operator != 'default' and operator not in valid_operators:
                    exit('[-] operator: [{}] must in [{}]'.format(operator, ','.join(valid_operators)))
                if ranges and ranges != 'default' and operator != 'append' and not re.findall('(<|>|=)=?\d', ranges):
                    exit('[-] range: [{}] is invalid'.format(ranges))
                ele.append(position if position else 'default')
                ele.append(operator if operator else 'default')
                ele.append(ranges if ranges else 'default')
            elements.append(ele)
        result.append(elements)
    return result


def chinese_2_pinyin(chinese_file):
    chinese_list = []
    chinese_pinyin_list = []
    if not os.path.isfile(chinese_file):
        exit("[-] File: {} not exists".format(chinese_file))
    with io.open(chinese_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            chinese_list.append(line.strip())
    for chinese in chinese_list:
        py = lazy_pinyin(chinese)
        chinese_pinyin_list.append(py)
    return chinese_pinyin_list


def parse_pattern(name_lists, pattern):
    rs = []
    real_length = len(pattern)
    for p in pattern:
        if 'append' in "".join(p):
            real_length -= 1
    for name_list in name_lists:
        if len(name_list) == real_length:
            rs.append(parse_operator(name_list, pattern))
    return rs


# order preserving
def unique(seq, idfun=None):
    if idfun is None:
        def idfun(x): return x
    rs = []
    seen = {}
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        rs.append(item)
    return rs


def finish_counter(store_path):
    line_count = 0
    with open(store_path, 'r') as files:
        for _ in files:
            line_count += 1
    return line_count


def finish_printer(store_path):
    count = finish_counter(store_path)
    print("[+] A total of : {0:} lines\n"
          "[+] Store in   : {1} \n"
          "[+] Cost       : {2} seconds".format(count, store_path, str(time.time() - start_time)[:6]))


if __name__ == "__main__":
    start_time = time.time()
    banner = r'''
                  ___  __  __  ____ 
                 / __)(  \/  )(  _ \
                ( (__  )    (  )   /
                 \___)(_/\/\_)(_)\_)        CMR v0.1
'''
    print(banner)
    try:
        current_dir = os.path.dirname(os.path.join(os.path.abspath(sys.argv[0]))).encode('utf-8').decode()
    except UnicodeError:
        try:
            current_dir = os.path.dirname(os.path.abspath(sys.argv[0])).decode('utf-8')
        except UnicodeError:
            current_dir = "."
            exit('[*] Please apply this script in ascii path')
    output_path = os.path.join(current_dir, 'output')
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input',
                        default=os.path.join(current_dir, 'wordlist', 'top-500-chinese-name.txt'),
                        help='input chinese names file path, default: top-500-chinese-name.txt')
    parser.add_argument('-p', '--pattern', dest='pattern', default='{::}{::},{::}{::}{::}',
                        help='chinese pinyin generation pattern, default: {::}{::},{::}{::}{::}')
    parser.add_argument('-o', '--output', dest='output', default='', help='output path')
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    valid_operators = ['default', 'upper', 'lower', 'reverse', 'append', 'remove']
    input_file = args.input
    pattern_string = args.pattern
    output_path = args.output if args.output else os.path.join(output_path, str(time.time())[-6:] + '.txt')
    if not os.path.isfile(input_file):
        exit('[-] input file: [{}] not exists'.format(input_file))
    patterns_list = prepare_pattern(pattern_string)
    pinyin_list = chinese_2_pinyin(input_file)
    results = []
    for patterns in patterns_list:
        results.extend(parse_pattern(pinyin_list, patterns))
    with io.open(output_path, 'w') as f:
        for r in unique(results):
            try:
                f.write(r + '\n')
            except TypeError:
                f.write(unicode(r) + '\n')
    finish_printer(output_path)
