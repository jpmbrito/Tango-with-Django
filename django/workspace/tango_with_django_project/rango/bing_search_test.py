import sys
import getopt
from bing_search import run_query

def main(argv):
    for query in argv:
        print "Searching for {0}".format(query)
        results = run_query(query)
        i = 1
        for result in results:
            print "({0}) - {1} - {2}".format(
                i,
                result['title'],
                result['link']
                )
            i = i + 1

if __name__ == "__main__":
    main(sys.argv[1:])