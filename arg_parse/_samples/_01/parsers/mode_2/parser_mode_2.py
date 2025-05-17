from arg_parse._samples._01.enums import ModeType, MetaType
from arg_parse._samples._01.parsers.mode_2.parser_mode_2_action_1 import ParserMode2Action1
from arg_parse._samples._01.parsers.mode_2.parser_mode_2_action_2 import ParserMode2Action2
from arg_parse.ifaces import IParser


class ParserMode2(IParser):

    def add_args(self, parent_parser):

        sub_parsers = [
            ParserMode2Action1(),
            ParserMode2Action2()
        ]

        parser = parent_parser.add_parser(
            description="Mode 2.",
            name=ModeType.MODE_2,
            help="Mode 2 help.")

        action_parsers = parser.add_subparsers(
            dest=MetaType.ACTION,
            help="Action to take.",
            required=True)

        for sub_parser in sub_parsers:
            sub_parser.add_args(action_parsers)

        return parser


