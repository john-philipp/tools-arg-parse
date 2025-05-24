from arg_parse._samples._01.enums import Mode, MetaType
from arg_parse._samples._01.parser_defs.mode_1.parser_def_mode_1_action_1 import ParserDefMode1Action1
from arg_parse._samples._01.parser_defs.mode_1.parser_def_mode_1_action_2 import ParserDefMode1Action2
from arg_parse.ifaces import IParserDef


class ParserDefMode1(IParserDef):

    def register_args(self, parent_parser):

        sub_parsers = [
            ParserDefMode1Action1(),
            ParserDefMode1Action2()
        ]

        parser = parent_parser.add_parser(
            description="Mode 1.",
            name=Mode.MODE_1,
            help="Mode 1 help.")

        action_parsers = parser.add_subparsers(
            dest=MetaType.ACTION,
            help="Action to take.",
            required=True)

        for sub_parser in sub_parsers:
            sub_parser.register_args(action_parsers)

        return parser


