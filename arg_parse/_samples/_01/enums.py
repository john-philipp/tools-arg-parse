from arg_parse.ifaces import IEnum


class MetaType(IEnum):
    ACTION = "action"
    MODE = "mode"


class Mode(IEnum):
    MODE_1 = "mode_1"
    MODE_2 = "mode_2"


class Mode1Action(IEnum):
    ACTION_1 = "action_1"
    ACTION_2 = "action_2"


class Mode2Action(IEnum):
    ACTION_1 = "action_1"
    ACTION_2 = "action_2"


class RequiredArg(IEnum):
    VALUE_1 = 1
    VALUE_2 = 2


class OptionalIntArg(IEnum):
    @classmethod
    def valid(cls, value):
        return isinstance(value, int)


