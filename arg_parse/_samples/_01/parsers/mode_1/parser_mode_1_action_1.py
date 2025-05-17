from arg_parse._samples._01.enums import Mode1ActionType
from arg_parse.ifaces import IParser


class ParserMode1Action1(IParser):

    def add_args(self, parent_parser):

        parser = parent_parser.add_parser(
            description="Mode 1 action 1.",
            name=Mode1ActionType.ACTION_1)

        parser.add_argument(
            "--required-arg", "-r",
            help="A required arg for mode 1 action 1.",
            required=True)

        return parser
