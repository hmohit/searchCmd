import readline
from argparse import ArgumentParser,FileType
import atexit


HISTORY_FILE=".cmd_hist"

def parse_options():
    """Parses the command line arguments"""
    parser = ArgumentParser(description='Search commands from database')
    parser.add_argument('-f', '--filename', type=FileType('r'), help='file path to command list')
    parser.add_argument('-a', '--add', help='enter command to'
                                                            'be added')
    return parser.parse_args()

def main():
    args = parse_options()
    try:
        readline.read_history_file(HISTORY_FILE) 
    except IOError:
        pass
    readline.parse_and_bind("tab: complete")
    if args.add:
        readline.add_history(args.add)
    if args.filename:
        for line in args.filename:
            readline.add_history(line)
    if not args.add and not args.filename:
        while True:
            s = raw_input('>')
            if s is 'q':
                readline.remove_history_item(readline.get_current_history_length()-1)
                quit()
atexit.register(readline.write_history_file, HISTORY_FILE)
    
if __name__ == '__main__':
    main()
