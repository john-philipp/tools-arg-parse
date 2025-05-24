from arg_parse._samples._01.enums import Mode1Action
from arg_parse.ifaces import IParserDef


class ParserDefMode1Action2(IParserDef):

    def register_args(self, parent_parser):

        parser = parent_parser.add_parser(
            description="Mode 1 action 2.",
            name=Mode1Action.ACTION_2)

        parser.add_argument(
            "--required-arg", "-r",
            help="A required arg for mode 1 action 2.",
            required=True)

        parser.add_argument(
            "--optional-int-arg", "-o",
            help="Optional int arg for mode 1 action 2.")

        return parser
