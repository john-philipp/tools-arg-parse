from arg_parse._samples._01.enums import ModeType, MetaType
from arg_parse._samples._01.parsers.mode_1.parser_mode_1_action_1 import ParserMode1Action1
from arg_parse._samples._01.parsers.mode_1.parser_mode_1_action_2 import ParserMode1Action2
from arg_parse.ifaces import IParser


class ParserMode1(IParser):

    def add_args(self, parent_parser):

        sub_parsers = [
            ParserMode1Action1(),
            ParserMode1Action2()
        ]

        parser = parent_parser.add_parser(
            description="Mode 1.",
            name=ModeType.MODE_1,
            help="Mode 1 help.")

        action_parsers = parser.add_subparsers(
            dest=MetaType.ACTION,
            help="Action to take.",
            required=True)

        for sub_parser in sub_parsers:
            sub_parser.add_args(action_parsers)

        return parser


