import argparse

from arg_parse.ifaces import IParser


class ParserMain(IParser):

    def __init__(
            self, arg_parser: argparse.ArgumentParser,
            sub_parsers: list[IParser] = None,
            top_level_dest_name: str = "mode"):

        super().__init__()
        self.arg_parser: argparse.ArgumentParser = arg_parser
        self.sub_parsers: list[IParser] = sub_parsers or []
        self.top_level_dest_name: str = top_level_dest_name

    def register_sub_parser(self, sub_parser):
        self.sub_parsers.append(sub_parser)

    def add_args(self, parent_parser):

        parser = parent_parser.add_subparsers(
            dest=self.top_level_dest_name,
            help="What would you like to do?",
            required=True)

        for sub_parser in self.sub_parsers:
            sub_parser.add_args(parser)

        return parser

    def parse_args(self, *args):
        self.add_args(self.arg_parser)
        return self.arg_parser.parse_args(args=args)
