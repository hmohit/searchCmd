from searchMetaData import SearchMetaData
from argparse import ArgumentParser
from pickle import dump, load


def main():
    parser = ArgumentParser(description='Search commands from database')
    parser.add_argument('-f', '--filename', required=False, help='file path to command list')
    parser.add_argument('-s', '--search', required=False, help='enter search string')
    parser.add_argument('-S', '--searchDict', required=False, help='enter '
                                                                   'search string')
    parser.add_argument('-a', '--add', required=False, help='enter command to'
                                                            'be added')

    try:
        args = parser.parse_args()

        try:
            delegate = load(open('metadata.raw', 'rb'))

        except Exception:
            delegate = SearchMetaData()
        if args.filename:
            delegate.load_new_commands(filename=args.filename)
            delegate.create_dict()
            dump(delegate, open('metadata.raw', 'wb'))

        elif args.search:
            for cmd in delegate.search(args.search):
                print cmd

        elif args.searchDict:
            print 'We have following commands for your requested search ' + args.searchDict

            for cmd in delegate.search_dict(args.searchDict):
                print cmd

    except Exception as err:
        print err


if __name__ == '__main__':
    main()
