import argparse

from arg_parse.ifaces import IParserDef


class ParserDefMain(IParserDef):

    def __init__(self, top_level_dest_name: str = "mode"):
        self._top_level_dest_name: str = top_level_dest_name
        self._sub_parsers = []

    def register_sub_parser(self, sub_parser_def: IParserDef):
        self._sub_parsers.append(sub_parser_def)

    def register_args(self, parser: argparse.ArgumentParser):
        sub_parsers = parser.add_subparsers(
            dest=self._top_level_dest_name,
            help="What would you like to do?",
            required=True)

        for sub_parser in self._sub_parsers:
            sub_parser.register_args(sub_parsers)

        return sub_parsers
