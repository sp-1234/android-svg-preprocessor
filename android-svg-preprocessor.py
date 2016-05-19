#!/usr/bin/env python3

import os
from os import path
import shlex
import shutil
import argparse
from shlex import quote

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
    import subprocess as sp
    return_code = sp.Popen(command).wait()
    assert return_code == 0


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', '-p', default=DEFAULT_TARGET_PATH,
                    help='the resources path, default is %s' % DEFAULT_TARGET_PATH)

    ap.add_argument('--prefix', default=DEFAULT_PREFIX,
                    help='the resources path, default is %s' % DEFAULT_TARGET_PATH)

    ap.add_argument('input_files', nargs='+', help='input images (SVG)')
    return ap.parse_args()


def basename_no_ext(full_path):
    return os.path.splitext(os.path.basename(full_path))[0]


def process_file_for_dpi(dpi_name, dpi_scale, input_file, output_path, prefix):
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
    render_density = 90 * dpi_scale
    cmd = [
        'convert',
        '-density', str(render_density),
        '-background', 'none',
        input_file,
        '-depth', '8',
        output_file_path
    ]
    sh(cmd)


def process_file(input_file, output_path, prefix):
    for dpi_name, dpi_scale in DPIS.items():
        process_file_for_dpi(dpi_name, dpi_scale, input_file, output_path, prefix)


def do_process(inputs, output_path, prefix):
    for input_file in inputs:
        process_file(input_file, output_path, prefix)


def main():
    ap = parse_args()
    inputs = ap.input_files
    output_path = ap.path
    prefix = ap.prefix
    do_process(inputs, output_path, prefix)


if __name__ == '__main__':
    main()
