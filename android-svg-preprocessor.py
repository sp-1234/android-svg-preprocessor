#!/usr/bin/env python3

import os
from os import path
import shlex
import shutil
import argparse

DEFAULT_TARGET_PATH = os.getcwd()


def sh(command: str):
    import subprocess as sp
    return_code = sp.Popen(command, shell=True).wait()
    assert return_code == 0


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', '-p', default=DEFAULT_TARGET_PATH,
                    help='the resources path, default is %s' % DEFAULT_TARGET_PATH)

    ap.add_argument('input_files', nargs='+', help='input images (SVG)')
    return ap.parse_args()


def main():
    ap = parse_args()
    inputs = ap.input_files
    output_path = ap.path
    print(inputs)


if __name__ == '__main__':
    main()
