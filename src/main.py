import getopt
import sys

import drawer
import getter


def main(argv):
    username, limit = '', None
    help_string = 'analyze -u <username> -l <limit>'
    try:
        opts, args = getopt.getopt(argv, "hu:l:", ["username=", "limit="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_string)
            sys.exit(0)
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-l", "--limit"):
            # if limit is None:  # or type(limit) != int:
            #     limit = 20
            # else:
            limit = arg
        else:
            print(help_string)
            sys.exit(0)
    return drawer.draw_countries(getter.get_countries(username, limit), username)


if __name__ == '__main__':
    main(sys.argv[1:])
