# Need to explicitly import enums to have them accessible for validation.
from arg_parse._samples._01.enums import *
from arg_parse.ifaces import Args


class AppArgs(Args):
    def __init__(self):
        super().__init__(globals())
        self.required_arg = RequiredArg.VALUE_1
        self.optional_int_arg = 123
