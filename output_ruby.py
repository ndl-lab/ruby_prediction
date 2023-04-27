

# Copyright (c) 2023, National Diet Library, Japan
#
# This software is released under the CC BY 4.0.
# https://creativecommons.org/licenses/by/4.0/

import argparse
import copy
import re
import xml.etree.ElementTree as ET
import Mykytea
import regex
import time
import pathlib

find_kanzi = regex.compile(r'[\p{Script=Han}]')
opt = ""
kytea = Mykytea.Mykytea(opt)
find_sentence = re.compile('.*[。?!？！]')
LIMIT_SIZE = 50


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml',
                        help='input xml',
                        type=pathlib.Path)
    parser.add_argument('-t', '--timetest',
                        action='store_true',
                        help="timetest")
    return parser.parse_args()


def kz2hr(orig, hira, output):
    if hira == 'UNK':
        return output + orig
    if find_kanzi.search(orig):
        return output + hira
    return output + orig


def make_output(sentence):
    if not sentence:
        return None

    out = ""
    kytea_result = kytea.getTagsToString(sentence).split(" ")
    for result in kytea_result[:len(kytea_result)-1]:
        result = result.split("/")
        if len(result) >= 3:
            orig = result[0]
            hira = result[2]
        else:
            orig = hira = result[0]
        out = kz2hr(orig, hira, out)
    print(out)


def make_output_with_cli(sentence, kytea_only=False):
    if not sentence:
        return None

    out = ""
    kytea_result = kytea.getTagsToString(sentence).split(" ")
    for result in kytea_result[:-1]:
        result = result.split("/")
        if len(result) >= 3:
            orig = result[0]
            hira = result[2]
        else:
            orig = hira = result[0]
        out = kz2hr(orig, hira, out)
    return out


def extract_sentence(text):
    if find_sentence.findall(text):
        sentence = find_sentence.findall(text)[0]
        text = text[len(sentence):]
        return sentence, text
    if len(text) > LIMIT_SIZE:
        sentence = text
        text = ""
        return sentence, text
    return False, text


def output_hira(input_xml, timetest=False):
    proc_times = []
    tree = ET.parse(input_xml)
    root = tree.getroot()
    XMLNS = ''
    m = re.search('{.*}', root.tag)
    if m:
        XMLNS = m.group(0)
    for page in root:
        if timetest:
            prev_time = time.perf_counter()
        for block in page:
            text_pool = ""
            for elm in block:
                if elm.tag == XMLNS + "LINE":
                    text_pool = text_pool + elm.attrib['STRING']
                    sentence, text_pool = extract_sentence(text_pool)
                    make_output(sentence)
            make_output(text_pool)
        print(page.attrib['IMAGENAME'])
        if timetest:
            proc_time = time.perf_counter() - prev_time
            print("processing time: {}ms".format(proc_time*1000))
            proc_times.append(proc_time)
    return proc_times


def output_hira_with_cli(input_data):
    output_data = copy.deepcopy(input_data)
    root = input_data['xml'].getroot()

    output_str = ''
    XMLNS = ''
    m = re.search('{.*}', root.tag)
    if m:
        XMLNS = m.group(0)
    for page in root:
        for elm in page.iter('LINE'):
            text_pool = ""
            if elm.tag == XMLNS + "LINE":
                text_pool = text_pool + elm.attrib['STRING']
                sentence, text_pool = extract_sentence(text_pool)
                ruby_str = make_output_with_cli(sentence, kytea)
                if ruby_str is not None:
                    output_str += ruby_str
                    output_str += '\n'
            ruby_str = make_output_with_cli(text_pool)
            if ruby_str is not None:
                output_str += ruby_str
                output_str += '\n'
    output_data['ruby_txt'] = output_str
    return output_data


if __name__ == '__main__':
    args = parse_args()
    sum_time = []
    try:
        if args.xml.is_dir():
            file_pathes = args.xml.glob("*.xml")
            for path in file_pathes:
                sum_time += output_hira(path, args.timetest)
            if args.timetest:
                print("\nTimeTestResult")
                avg_time = sum(sum_time)/len(sum_time) * 1000
                print("average processing time: {}ms".format(avg_time))
        else:
            output_hira(args.xml, args.timetest)

    except SyntaxError:
        print("Input file path '{}' is not appropriate.".format(args.xml))
