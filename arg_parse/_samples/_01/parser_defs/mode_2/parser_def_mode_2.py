from arg_parse._samples._01.enums import Mode, MetaType
from arg_parse._samples._01.parser_defs.mode_2.parser_def_mode_2_action_1 import ParserDefMode2Action1
from arg_parse._samples._01.parser_defs.mode_2.parser_def_mode_2_action_2 import ParserDefMode2Action2
from arg_parse.ifaces import IParserDef


class ParserDefMode2(IParserDef):

    def register_args(self, parent_parser):

        sub_parsers = [
            ParserDefMode2Action1(),
            ParserDefMode2Action2()
        ]

        parser = parent_parser.add_parser(
            description="Mode 2.",
            name=Mode.MODE_2,
            help="Mode 2 help.")

        action_parsers = parser.add_subparsers(
            dest=MetaType.ACTION,
            help="Action to take.",
            required=True)

        for sub_parser in sub_parsers:
            sub_parser.register_args(action_parsers)

        return parser


