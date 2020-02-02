import argparse
import sys

from gyazo_backup.backup import backup


def main():
    parser = argparse.ArgumentParser(description="Python Gyazo Backup")
    parser.add_argument('--token', dest='access_token', required=True,
                        help='API access token')
    parser.add_argument(
        '--threads', dest='num_threads', default=8, type=int,
        help='number of threads for downloading images (default: 8)')
    parser.add_argument('directory', help='backup destination')
    result = backup(parser.parse_args())
    sys.exit(result)
