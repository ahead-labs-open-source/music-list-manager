import argparse
from . import extract, tag, rename, convert

def main():
    parser = argparse.ArgumentParser(prog='music-list', description='Music list manager (extraction, tagging, renaming, conversion).')
    sub = parser.add_subparsers(dest='command', required=True)

    p_ext = sub.add_parser('extract', help='Extract metadata from HTML to CSV.')
    p_ext.add_argument('--html', default='music_list_source.html')
    p_ext.add_argument('--csv', default='music_list.csv')

    p_tag = sub.add_parser('tag', help='Apply ID3 tags and covers to MP3 files.')
    p_tag.add_argument('--csv', default='music_list.csv')
    p_tag.add_argument('--dir', default='Music_List')

    p_ren = sub.add_parser('rename', help='Rename files according to CSV.')
    p_ren.add_argument('--csv', default='music_list.csv')
    p_ren.add_argument('--dir', default='Music_List')

    p_conv = sub.add_parser('convert', help='Convert WAV to MP3.')
    p_conv.add_argument('--in', dest='in_dir', default='Music_WAV')
    p_conv.add_argument('--out', dest='out_dir', default='Music_MP3')
    p_conv.add_argument('--bitrate', default='320k')

    args = parser.parse_args()

    if args.command == 'extract':
        extract.main(args.html, args.csv)
    elif args.command == 'tag':
        tag.main(args.csv, args.dir)
    elif args.command == 'rename':
        rename.main(args.csv, args.dir)
    elif args.command == 'convert':
        convert.main(args.in_dir, args.out_dir, args.bitrate)
