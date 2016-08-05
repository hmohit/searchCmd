from searchMetaData import SearchMetaData
from argparse import ArgumentParser


def main():
    try:
        parser = ArgumentParser()
        parser.add_argument('-f', '--filename', required=True)
        args = vars(parser.parse_args())
        delegate = SearchMetaData()
        delegate.load_new_commands(filename=args['file_name'])

    except Exception as err:
        print err


if __name__ == '__main__':
    main()
