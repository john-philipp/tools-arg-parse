import argparse
import logging
import os
import sys

from arg_parse._samples._01.args.args import AppArgs
from arg_parse._samples._01.parser_defs.mode_1.parser_def_mode_1 import ParserDefMode1
from arg_parse._samples._01.parser_defs.mode_2.parser_def_mode_2 import ParserDefMode2
from arg_parse.arg_parser import ArgParser
from arg_parse.parser_def_main import ParserDefMain


log = logging.getLogger(__name__)


def get_args_path():
    args_path = "args/args.yml"
    if not os.path.isfile(args_path):
        args_path = os.path.join("arg_parse/_samples/_01/args/args.yml")
    return args_path


def get_env_var_prefix():
    return "SAMPLE"


if __name__ == '__main__':
    os.environ["SAMPLE_REQUIRED_ARG"] = "2"
    args = sys.argv[1:]
    if not args:
        args = ["mode_1", "action_2", "-r", "1"]

    base_parser = argparse.ArgumentParser(
        prog="arg-parse",
        description="Sample code.")

    parser_def = ParserDefMain()
    parser_def.register_sub_parser(ParserDefMode1())
    parser_def.register_sub_parser(ParserDefMode2())
    parser_def.register_args(base_parser)

    arg_parser = ArgParser(
        args_cls=AppArgs,
        from_file_path=get_args_path(),
        from_env_prefix=get_env_var_prefix())

    parsed_args = arg_parser.parse_args(base_parser, *args)
    parsed_args.log()

