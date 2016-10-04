#!/usr/bin/env python
import subprocess
import os
import sys
import readline
import threading

from searchMetaData import SearchMetaData
from argparse import ArgumentParser
from pickle import dump, load


def write_to_clipboard(output):
    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


def main():
    parser = ArgumentParser(description='Search commands from database')
    parser.add_argument('-f', '--filename', required=False, help='file path to command list')
    parser.add_argument('-s', '--search', required=False, action='store_true', help='enter search string')
    #parser.add_argument('-s', '--search', required=False, type=str, help='enter search string')
    parser.add_argument('-l', '--ls', required=False, action='store_true', help='enter search string')

    mutex_group1 = parser.add_mutually_exclusive_group()
    mutex_group1.add_argument('-a', '--add', required=False, nargs='+', type=str,
                              help='enter commands followed by optional tags')
    mutex_group1.add_argument('-d', '--delete', help='enter command to be deleted')
    meta_file = os.path.join(os.path.dirname(__file__), 'metadata.raw')

    try:
        args = parser.parse_args()

        try:
            delegate = load(open(meta_file, 'rb'))

        except StandardError:
            delegate = SearchMetaData()

        if args.filename:
            delegate.load_new_commands(filename=args.filename)
            dump(delegate, open(meta_file, 'wb'))

        elif args.delete:
            results = delegate.search(args.delete)
            for k, v in enumerate(results):
                print k, ':', v

            if results:
                inp = raw_input('Delete cmd num: ').strip()
                if inp:
                    try:
                        index = map(int, inp.split('-'))
                    except StandardError:
                        print "Input should be number or number-number"
                        return
                    if len(index) == 1:
                        start, end = index[0], index[0] + 1
                    else:
                        start, end = index[0], index[1] + 1
                    for idx in range(start, end):
                        delegate.delete(results[idx])

                    dump(delegate, open(meta_file, 'wb'))

        elif args.search:
            t = threading.Thread(target=dyn_search, args=(delegate,))
            t.start()
            in_str = raw_input('>')
            t.join()
            search_str(in_str.strip(), delegate, 1)

            '''results = delegate.search(args.search)
            for index, cmd in enumerate(results):
                print index, ':', cmd

            if results:
                inp = raw_input('Enter cmd to cpy to clipboard ').strip()
                try:
                    index = int(inp)
                except StandardError:
                    if inp:
                        print "Input should be number "
                    return

                write_to_clipboard(results[index])
                delegate.insert_in_cache(results[index])
                dump(delegate, open(meta_file, 'wb'))
                '''

        elif args.add:
            delegate.add_command(args.add[0], set(args.add[1:]))
            dump(delegate, open(meta_file, 'wb'))

        elif args.ls:
            print delegate

    except Exception as err:
        print err


def dyn_search(delegate):
    last_str = ''
    while True:
        in_str = readline.get_line_buffer()
        if in_str and in_str[-1] == '\n':
            exit()
        if last_str != in_str:
            print
            last_str = in_str
            search_str(in_str, delegate)
            print '>', in_str,
            sys.stdout.flush()


def search_str(input_str, delegate, last=0):
    results = delegate.search(input_str)
    for index, cmd in enumerate(results):
        sys.stdout.write('\033[K')
        print index, ':', cmd
    if not last:
        sys.stdout.write(('\033[K\n')*(5-len(results)))
        sys.stdout.write('\033[6A')
    #sys.stdout.write('\033[6A')
    sys.stdout.flush()
    #if results:
    #    inp = raw_input('Enter cmd to cpy to clipboard ').strip()
    #    try:
    #        index = int(inp)
    #    except:
    #        if inp:
    #            print "Input should be number "
    #        return


if __name__ == '__main__':
    main()
