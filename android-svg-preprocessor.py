#!/usr/bin/env python3

import argparse
import os

DEFAULT_TARGET_PATH = os.getcwd()
DEFAULT_PREFIX = 'drawable'

DPIS = {
    'xxxhdpi': 4,
    'mdpi': 1,
    'hdpi': 1.5,
    'xhdpi': 2,
    'xxhdpi': 3,
    'tvdpi': 1.33
}


def sh(command):
    print('Running shell command:')
    print(command)
    print('\n')
    import subprocess as sp
    return_code = sp.Popen(command).wait()
    assert return_code == 0


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', '-p', default=DEFAULT_TARGET_PATH,
                    help='the resources path, default is %s' % DEFAULT_TARGET_PATH)

    ap.add_argument('--prefix', default=DEFAULT_PREFIX,
                    help='prefix, default is %s' % DEFAULT_PREFIX)
    ap.add_argument('--scale', default='1')

    ap.add_argument('input_files', nargs='+', help='input images (SVG)')
    return ap.parse_args()


def basename_no_ext(full_path):
    return os.path.splitext(os.path.basename(full_path))[0]


def process_file_for_dpi(dpi_name, dpi_scale, input_file, output_path, prefix, scale):
    resource_name = basename_no_ext(input_file)
    output_path = os.path.join(
        output_path,
        "{}-{}".format(prefix, dpi_name)
    )
    os.makedirs(output_path, exist_ok=True)
    output_file_path = os.path.join(
        output_path,
        resource_name + ".png"
    )
    render_density = dpi_scale * scale
    dpi_string = str(render_density)
    cmd = [
        'rsvg-convert',
        '-z', dpi_string,
        '-o', output_file_path,
        input_file
    ]
    sh(cmd)


def process_file(input_file, output_path, prefix, scale):
    for dpi_name, dpi_scale in DPIS.items():
        process_file_for_dpi(dpi_name, dpi_scale, input_file, output_path, prefix, scale)


def do_process(inputs, output_path, prefix, scale):
    for input_file in inputs:
        process_file(input_file, output_path, prefix, scale)


def main():
    ap = parse_args()
    inputs = ap.input_files
    output_path = ap.path
    prefix = ap.prefix
    scale = float(ap.scale)
    do_process(inputs, output_path, prefix, scale)


if __name__ == '__main__':
    main()
