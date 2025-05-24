from arg_parse._samples._01.enums import Mode1Action
from arg_parse.ifaces import IParserDef


class ParserDefMode1Action1(IParserDef):

    def register_args(self, parent_parser):

        parser = parent_parser.add_parser(
            description="Mode 1 action 1.",
            name=Mode1Action.ACTION_1)

        parser.add_argument(
            "--required-arg", "-r",
            help="A required arg for mode 1 action 1.",
            required=True)

        parser.add_argument(
            "--optional-int-arg", "-o",
            help="Optional int arg for mode 1 action 1.",
            default=0)

        return parser
