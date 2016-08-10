from searchMetaData import SearchMetaData
from argparse import ArgumentParser
from pickle import dump, load


def main():
    parser = ArgumentParser(description='Seach commands from database')
    parser.add_argument('-f', '--filename', required=False, help='file path to command list')
    parser.add_argument('-s', '--search', required=False, help='enter search string')
    parser.add_argument('-a', '--addcmd', required=False, help='enter command to'
                                                               'be added')

    try:
        args = vars(parser.parse_args())

        try:
            delegate = load(open('metadata.raw', 'rb'))

        except Exception as err:
            delegate = SearchMetaData()

        if args['filename'] is not '':
            delegate.load_new_commands(filename=args['filename'])
            dump(delegate, open('metadata.raw', 'wb'))

        elif args['search'] is not '':
            for cmd in delegate.search(args['search']):
                print cmd

    except Exception as err:
        print "error"
        print err


if __name__ == '__main__':
    main()
