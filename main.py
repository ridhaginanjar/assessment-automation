import argparse
import os.path

from pipeline.index import main


def check_is_dir(directory_path):
    if not os.path.isdir(directory_path):
        raise argparse.ArgumentTypeError('{} is not a directory'.format(directory_path))
    return directory_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", type=check_is_dir, help="Input report.json path", required=True)
    parser.add_argument("-s", type=check_is_dir, help="Input Submission Path", required=True)

    args = parser.parse_args()

    main(args)
