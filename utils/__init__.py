import argparse


def get_commandline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-shairport', action='store_true', help='Indicates whether audio will be played over shairport or not')

    args = parser.parse_args()
    return args