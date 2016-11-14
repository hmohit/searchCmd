#!/usr/bin/env python

# Put future imports here
from __future__ import division

# Put Python imports here
import os
import sys
import threading
import time
import argparse
import pickle

# Put searchCmd imports here
from searchMetaData import SearchMetaData
from keys import DisplayBuffer
from keys import GetCharacter
from keys import write_to_clipboard


def cached_search(search_str, delegate):
    results = delegate.search(search_str)
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


def type_ahead_search(delegate):
    get_character = GetCharacter()
    display_content = DisplayBuffer(delegate)

    while display_content.cont:
        display_content.execute_key_handler(get_character())

    delegate.insert_in_cache(display_content.selected)


def dynamic_search(delegate):
    done_event = threading.Event()
    t = threading.Thread(target=delegate.dyn_search, args=(done_event,))
    t.setDaemon(True)
    t.start()

    try:
        raw_input('>')
        sys.stdout.write('\033[A')

    except KeyboardInterrupt:
        exit()

    finally:
        done_event.set()
        while threading.active_count() > 1:
            time.sleep(0.01)


def main():
    parser = argparse.ArgumentParser(description='Search commands from database')
    parser.add_argument('-f', '--filename', required=False, help='file path to command list')
    parser.add_argument('-s', '--search', required=False, action='store_true', help='enter search string')
    parser.add_argument('-l', '--ls', required=False, action='store_true', help='enter search string')

    mutex_group1 = parser.add_mutually_exclusive_group()
    mutex_group1.add_argument('-a', '--add', required=False, nargs='+', type=str,
                              help='enter commands followed by optional tags')
    mutex_group1.add_argument('-d', '--delete', help='enter command to be deleted')
    meta_file = os.path.join(os.path.dirname(__file__), 'metadata.raw')

    try:
        args = parser.parse_args()

        try:
            delegate = pickle.load(open(meta_file, 'rb'))

        except StandardError:
            delegate = SearchMetaData()

        if args.filename:
            delegate.load_new_commands(filename=args.filename)
            pickle.dump(delegate, open(meta_file, 'wb'))

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

                    pickle.dump(delegate, open(meta_file, 'wb'))

        elif args.search:
            type_ahead_search(delegate)
            pickle.dump(delegate, open(meta_file, 'wb'))

        elif args.add:
            delegate.add_command(args.add[0], set(args.add[1:]))
            pickle.dump(delegate, open(meta_file, 'wb'))

        elif args.ls:
            print delegate

    except Exception as err:
        print err


if __name__ == '__main__':
    main()
