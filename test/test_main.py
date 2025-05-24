import argparse
import os
import unittest

from arg_parse._samples._01.args.args import AppArgs
from arg_parse._samples._01.parser_defs.mode_1.parser_def_mode_1 import ParserDefMode1
from arg_parse._samples._01.parser_defs.mode_2.parser_def_mode_2 import ParserDefMode2
from arg_parse._samples._01.run import get_env_var_prefix
from arg_parse.arg_parser import ArgParser
from arg_parse.make_docs import make_docs
from arg_parse.parser_def_main import ParserDefMain


def get_args_path():
    args_path = "../arg_parse/_samples/_01/args/args.yml"
    if not os.path.isfile(args_path):
        args_path = os.path.join("arg_parse/_samples/_01/args/args.yml")
    return args_path


class TestMain(unittest.TestCase):

    def test_main(self):
        os.environ["SAMPLE_REQUIRED_ARG"] = "2"
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

        # Just for coverage.
        make_docs(base_parser)