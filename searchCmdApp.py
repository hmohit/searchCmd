#!/usr/bin/python
from searchMetaData import SearchMetaData
from argparse import ArgumentParser
from pickle import dump, load
import os


def main():
    parser = ArgumentParser(description='Search commands from database')
    parser.add_argument('-f', '--filename', help='file path to command list')
    parser.add_argument('-s', '--search', help='enter search string')
    parser.add_argument('-S', '--searchDict', help='enter search string')
    mutex_group1= parser.add_mutually_exclusive_group()
    mutex_group1.add_argument('-a', '--add', help='enter command to be added')
    mutex_group1.add_argument('-d', '--delete', action='store_true',
                              help='enter command to be added')
    meta_file = os.path.join(os.path.dirname(__file__), 'metadata.raw')
    try:
        args = parser.parse_args()

        try:
            delegate = load(open(meta_file, 'rb'))

        except Exception:
            delegate = SearchMetaData()
        if args.filename:
            delegate.load_new_commands(filename=args.filename)
            delegate.create_dict()
            dump(delegate, open(meta_file, 'wb'))

        elif args.delete:
            results = delegate.search(args.search)
            for k,v  in enumerate(results):
                print k, ':', v
            num = int(raw_input('Delete cmd num: '))
            delegate.delete(results[num])
            dump(delegate, open(meta_file, 'wb'))

        elif args.search:
            for cmd in delegate.search(args.search):
                print cmd

        elif args.searchDict:
            print 'We have following commands for your requested search ' + args.searchDict

            for cmd in delegate.search_dict(args.searchDict):
                print cmd

        elif args.add:
            delegate.add_command(args.add)
            dump(delegate, open(meta_file, 'wb'))

    except Exception as err:
        print err


if __name__ == '__main__':
    main()
