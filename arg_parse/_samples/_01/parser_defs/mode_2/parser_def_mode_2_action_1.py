from arg_parse._samples._01.enums import Mode2Action
from arg_parse.ifaces import IParserDef


class ParserDefMode2Action1(IParserDef):

    def register_args(self, parent_parser):

        parser = parent_parser.add_parser(
            description="Mode 2 action 1.",
            name=Mode2Action.ACTION_1)

        parser.add_argument(
            "--required-arg", "-r",
            help="A required arg for mode 2 action 1.",
            required=True)

        parser.add_argument(
            "--optional-int-arg", "-o",
            help="Optional int arg for mode 2 action 1.")

        return parser
