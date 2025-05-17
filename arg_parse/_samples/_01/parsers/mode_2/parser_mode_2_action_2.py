from arg_parse._samples._01.enums import Mode2ActionType
from arg_parse.ifaces import IParser


class ParserMode2Action2(IParser):

    def add_args(self, parent_parser):

        parser = parent_parser.add_parser(
            description="Mode 2 action 2.",
            name=Mode2ActionType.ACTION_2)

        parser.add_argument(
            "--required-arg", "-r",
            help="A required arg for mode 2 action 2.",
            required=True)

        return parser
