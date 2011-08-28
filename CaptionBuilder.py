#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
## @file CaptionBuilder.py
#  @brief "PROTOTYPE" caption builder for Python 3.2 or later.
#  @date 2011.08.28
import codecs
import sys
import os.path
import csv
import yaml
import subprocess
from optparse import OptionParser
from xml.etree.ElementTree import ElementTree

#------------------------------------------------------------------------------
## @brief main関数
#  @param[in] i_options   option値。
#  @param[in] i_arguments 引数list。
def _main(i_options, i_arguments):

    # 字幕resource-fileを読み込んで、字幕書庫を作成。
    a_archives = {}
    for a_path in i_arguments:
        print('Loading "' + a_path + '"')
        with open(a_path, mode='r', encoding='utf-8') as a_file:
            a_dummy, a_extension = os.path.splitext(a_path)
            if '.csv' == a_extension:
                _load_csv_captions(
                    a_archives,
                    a_file, 
                    i_options.source_lang,
                    i_options.target_lang)
            else:
                a_archives.update(yaml.load(a_file))

    # 字幕書庫から字幕文字集合を作成。
    a_font_chars = set()
    if not i_options.base_path:
        for a_captions in a_archives.values():
            for a_key, a_caption in a_captions.items():
                a_text = _get_caption_text(
                    a_key, 
                    a_caption,
                    i_options.source_lang,
                    i_options.target_lang)
                for a_char in a_text:
                    if 255 < ord(a_char):
                        a_font_chars.add(a_char)
    elif os.path.isdir(i_options.base_path):
        # 字幕書庫から字幕文字集合と字幕-fileを作成。
        for a_path, a_captions in sorted(a_archives.items()):
            a_font_chars.update(
                _build_captions_file(
                    a_captions,
                    os.path.normpath(
                        os.path.join(i_options.base_path, a_path)),
                    i_options.source_lang,
                    i_options.target_lang))
    else:
        # base-pathがdirectoryではないので停止。
        raise Exception(
            ''.join((
                'Path "', i_options.base_path, '" appointed with',
                'an option "--base_path" is not a directory.')))

    # 字幕文字集合から字幕fontを作成。
    if i_options.font_xml_path:
        _build_font_file(
            i_options.base_path, i_options.font_xml_path, a_font_chars)

    # 字幕csv-fileを作成。
    if i_options.out_csv_path:
        a_csv = csv.writer(
            open(
                i_options.out_csv_path,
                mode='w',
                encoding='utf-8',
                newline='\n'),
            lineterminator='\n')
        a_csv.writerow((
            'path', 'key', i_options.source_lang, i_options.target_lang))
        for a_path, a_captions in sorted(a_archives.items()):
            for a_key, a_caption in sorted(a_captions.items()):
                a_row = [a_path, a_key, a_caption.get(i_options.source_lang)]
                a_target_text = a_caption.get(i_options.target_lang)
                if a_target_text:
                    a_row.append(a_target_text)
                a_csv.writerow(a_row)

    # 字幕yaml-fileを作成。
    if i_options.out_yaml_path:
        yaml.dump(
            a_archives,
            open(
                i_options.out_yaml_path,
                mode='w',
                encoding='utf-8',
                newline='\n'),
            encoding='utf-8',
            width=0x7fffffff,
            allow_unicode=True,
            default_flow_style=False)

    print('complete!')

#------------------------------------------------------------------------------
## @brief 字幕csv-fileを読み込み、字幕書庫を更新する。
#  @param[in,out] io_archives   更新する字幕書庫。
#  @param[in]     i_file        読み込むcsv-file。
#  @param[in]     i_source_lang 原文の言語名。
#  @param[in]     i_target_lang 訳文の言語名。
def _load_csv_captions(io_archives, i_file, i_source_lang, i_target_lang):

    # headerを読み込む
    a_csv = csv.reader(i_file)
    a_iterator = iter(a_csv)
    a_header = next(a_iterator)
    a_path_index = a_header.index('path')
    a_key_index = a_header.index('key')
    a_source_index = a_header.index(i_source_lang)
    a_target_index = a_header.index(i_target_lang)

    # bodyを読み込む。
    for a_row in a_iterator:
        # 字幕書庫から字幕辞書を取得。
        a_path = a_row[a_path_index]
        a_captions = io_archives.get(a_path)
        if a_captions is None:
            a_captions = {}
            io_archives[a_path] = a_captions

        # 字幕辞書に字幕を登録。
        a_key = a_row[a_key_index]
        if a_key in a_captions:
            # a_pathの中にあるa_keyが重複しているので停止。
            raise Exception(
                ''.join((
                    'There is key "', a_key, '" repeating in path "',
                    a_path, '".')))
        a_caption = {}
        a_captions[a_key] = a_caption

        # 字幕に原文を登録。
        if a_source_index < len(a_row):
            a_source_text = a_row[a_source_index]
            if a_source_text:
                a_caption[i_source_lang] = a_source_text

        # 字幕に訳文を登録。
        if a_target_index < len(a_row):
            a_target_text = a_row[a_target_index]
            if a_target_text:
                a_caption[i_target_lang] = a_target_text

#------------------------------------------------------------------------------
## @brief 字幕文字列を取得。
def _get_caption_text(i_key, i_caption, i_source_lang, i_target_lang):
    a_text = i_caption.get(i_target_lang)
    if a_text is None:
        a_text = i_caption.get(i_source_lang)
        if a_text is None:
            # i_source_langとitarget_langの両方が字幕に見つからないので停止。
            raise Exception(
                ''.join((
                'There are not both "', i_source_lang,
                '" and "', i_target_lang,
                '" in a caption "', i_key, '".')))
    return a_text

#------------------------------------------------------------------------------
## @brief 字幕配列から字幕fileを作成。
def _build_captions_file(i_captions, i_base_path, i_source_lang, i_target_lang):

    # 字幕配列から字幕text-fileを作成。
    a_txt_path = i_base_path + '.txt'
    a_font_chars = set()
    with open(a_txt_path, mode='w', encoding='utf-8') as a_file:
        for a_key, a_caption in sorted(i_captions.items()):
            # 字幕を取得。
            a_text = _get_caption_text(
                a_key, a_caption, i_source_lang, i_target_lang)

            # 多バイト文字列の末尾が'!'だと文字化けするための対策。
            # 原因は不明。
            if 2 <= len(a_text) and '!' == a_text[-1] and 255 < ord(a_text[-2]):
                a_text = a_text[:-1] + '！'

            # 字幕textを書きだす。
            a_file.write(a_key + '=' + a_text + '\r\n')

            # 字幕文字辞書を更新。
            for a_char in a_text:
                if 255 < ord(a_char):
                    a_font_chars.add(a_char)

    # 字幕text-fileから字幕fileを作成。
    a_p3d_path = i_base_path + '.p3d'
    a_p3d_rz_path = a_p3d_path + '.rz'
    a_build_p3d = ('ProtoLE.exe', '-i', a_p3d_path)
    if os.path.isfile(a_p3d_rz_path):
        # p3d-fileを作成。
        subprocess.check_call((
            'offzip.exe', a_p3d_rz_path, a_p3d_path, '16'))
        subprocess.check_call(a_build_p3d)

        # p3d.rz-fileを作成。
        a_p3d_p3d_path = a_p3d_path + '.p3d'
        if os.path.isfile(a_p3d_p3d_path):
            os.remove(a_p3d_p3d_path)
        os.rename(a_p3d_path, a_p3d_p3d_path)
        subprocess.check_call(('PackageManager.exe', a_p3d_p3d_path))
        os.remove(a_p3d_p3d_path)

    elif os.path.isfile(a_p3d_path):
        # p3d-fileを作成。
        subprocess.check_call(a_build_p3d)
        os.remove(i_base_path + '.bak')

    os.remove(a_txt_path)
    return a_font_chars

#------------------------------------------------------------------------------
## @brief 字幕font-fileを作成。
def _build_font_file(i_base_path, i_template_xml_path, i_chars):
    a_latin_chars = ''.join((
        ' !"#$%&\'()*+,-./0123456789:;<=>?@',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'))

    # font-import-xml-fileを作成。
    print('Loading "' + i_template_xml_path + '"')
    a_template = ElementTree(
        file=open(i_template_xml_path, mode='r', encoding='utf-8'))
    a_font_import_xml = a_template.getroot().find('movie')
    a_font_define_xml = a_template.getroot().find('swf')
    a_target_fonts = a_font_define_xml.findall('.//DefineFont3')
    for a_font in a_font_import_xml.findall('.//font'):
        # font-tagのglyphs属性に、importする文字を設定。
        a_id = a_font.get('id')
        if a_id in ('subtitle', 'BodyPC', 'TitlePC'):
            a_chars = sorted(
                i_chars.difference(_make_font_chars(a_target_fonts, a_id)))
            a_font.set(
                'glyphs', ''.join((a_latin_chars, ''.join(a_chars))))
    a_xml_path = 'temp.fonts.xml'
    ElementTree(a_font_import_xml).write(
        a_xml_path, encoding='utf-8', method='xml', xml_declaration=True)

    # font-import-xml-fileからswf-fileを経由し、font定義xml-fileを作成。
    a_swf_path = 'temp.fonts.swf'
    print('Building "' + a_swf_path + '"')
    subprocess.check_call(('swfmill.exe', 'simple', a_xml_path, a_swf_path))
    print('Building "' + a_xml_path + '"')
    subprocess.check_call(('swfmill.exe', 'swf2xml', a_swf_path, a_xml_path))
    os.remove(a_swf_path)

    # font定義xml-fileからfont定義xmlを取り出す。
    a_font_source_xml = ElementTree(
        file=codecs.open(a_xml_path, mode='r', encoding='utf-8'))
    a_source_fonts = {}
    for a_symbol in a_font_source_xml.findall('.//Symbol'):
        a_id = int(a_symbol.get('objectID'))
        a_name = a_symbol.get('name')
        if a_name in ('subtitle', 'BodyPC', 'TitlePC'):
            a_source_fonts[a_id] = _make_font_name(a_name)
    for a_font in a_font_source_xml.findall('.//DefineFont3'):
        a_id = int(a_font.get('objectID'))
        a_key = a_source_fonts.get(a_id)
        if a_key is not None:
            del a_source_fonts[a_id]
            a_source_fonts[a_key] = a_font

    # font定義xmlと予約済みfont定義xmlを合成。
    for a_target_font in a_target_fonts:
        a_source_font = a_source_fonts.get(a_target_font.get('name'))
        if a_source_font is not None:
            # glyphs要素を合成。
            a_source_element = a_source_font.find('glyphs')
            a_target_element = a_target_font.find('glyphs')
            a_target_element.extend(a_source_element.getchildren())

            # advance要素を合成。
            a_source_element = a_source_font.find('advance')
            a_target_element = a_target_font.find('advance')
            a_target_element.extend(a_source_element.getchildren())

            # bounds要素を合成。
            a_target_element = a_target_font.find('bounds')
            a_source_element = a_source_font.find('bounds')
            a_target_element.extend(a_source_element.getchildren())

    # font定義xml-fileからfont-fileを作成。
    a_font_gfx_path = 'fonts_latin.gfx'
    if i_base_path:
        a_font_gfx_path = os.path.join('art/hud', a_font_gfx_path)
        a_font_gfx_path = os.path.normpath(
            os.path.join(i_base_path, a_font_gfx_path))
    print('Building "' + a_xml_path + '"')
    ElementTree(a_font_define_xml).write(
        a_xml_path, encoding='utf-8', method='xml', xml_declaration=True)
    print('Building "' + a_font_gfx_path + '"')
    subprocess.check_call((
        'swfmill.exe', 'simple', a_xml_path, a_font_gfx_path))

    os.remove(a_xml_path)

#------------------------------------------------------------------------------
def _make_font_chars(i_fonts, i_id):
    a_name = _make_font_name(i_id)
    a_chars = set()
    for a_font in i_fonts:
        if a_font.get('name') == a_name:
            for a_glyph in a_font.findall('.//Glyph'):
                a_chars.add(chr(int(a_glyph.get('map'))))
            break
    return a_chars

#------------------------------------------------------------------------------
def _make_font_name(i_name):
    return ''.join(('Prototype', i_name[0].upper(), i_name[1:]))

#------------------------------------------------------------------------------
## @brief command-line引数を解析。
#  @return option値と引数listのtuple。
def _parse_arguments(io_parser):
    io_parser.add_option(
        '-b',
        '--base',
        dest='base_path',
        help='set captions base directory path name')
    io_parser.add_option(
        '-c',
        '--csv',
        dest='out_csv_path',
        help='set output the captions csv-file path')
    io_parser.add_option(
        '-f',
        '--font',
        dest='font_xml_path',
        help='set the font template xml-file path')
    io_parser.add_option(
        '-s',
        '--source_lang',
        dest='source_lang',
        default='english',
        help='set the source language')
    io_parser.add_option(
        '-t',
        '--target_lang',
        dest='target_lang',
        default='japanese',
        help='set the target language')
    io_parser.add_option(
        '-y',
        '--yaml',
        dest='out_yaml_path',
        help='set output the captions yaml-file path')
    return io_parser.parse_args()

#------------------------------------------------------------------------------
if __name__ == "__main__":
    a_option_parser = OptionParser()
    a_options, a_arguments = _parse_arguments(a_option_parser)
    if a_arguments:
        _main(a_options, a_arguments)
    else:
        a_option_parser.print_help()
