import argparse
import sys

from arg_parse._samples._01.parsers.mode_1.parser_mode_1 import ParserMode1
from arg_parse._samples._01.parsers.mode_2.parser_mode_2 import ParserMode2
from arg_parse.make_docs import make_docs
from arg_parse.parser_main import ParserMain

if __name__ == '__main__':
    args = sys.argv[1:]
    arg_parser = argparse.ArgumentParser(
        prog="arg-parse",
        description="Sample code.")
    parser = ParserMain(arg_parser, [
        ParserMode1(),
        ParserMode2()])
    parsed_args = parser.parse_args(*args)

    make_docs(arg_parser)
    print(parsed_args.__dict__)

