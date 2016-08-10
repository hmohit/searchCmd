from searchMetaData import SearchMetaData
from argparse import ArgumentParser
from pickle import dump, load


def main():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file-name', required=False, help='file path to command list')
    parser.add_argument('-s', '--search', required=False, help='enter search string')
    parser.add_argument('-sd', '--search-dict', required=False, help='enter search string')

    try:
        args = vars(parser.parse_args())

        try:
            delegate = load(open('metadata.raw', 'rb'))

        except Exception as err:
            print err
            delegate = SearchMetaData()

        if args['file_name'] is not '':
            delegate.load_new_commands(filename=args['file_name'])
            delegate.create_dict()
            dump(delegate, open('metadata.raw', 'wb'))

        elif args['search'] is not '':
            print 'We have following commands for your requested search ' + args['search']

            for cmd in delegate.search(args['search']):
                print cmd

        elif args['search_dict'] is not '':
            print 'We have following commands for your requested search ' + args['search_dict']

            for cmd in delegate.search_dict(args['search_dict']):
                print cmd

    except Exception as err:
        print err


if __name__ == '__main__':
    main()
