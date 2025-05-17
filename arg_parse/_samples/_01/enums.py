from arg_parse.ifaces import IEnum


class MetaType(IEnum):
    ACTION = "action"
    MODE = "mode"


class ModeType(IEnum):
    MODE_1 = "mode_1"
    MODE_2 = "mode_2"


class Mode1ActionType(IEnum):
    ACTION_1 = "action_1"
    ACTION_2 = "action_2"


class Mode2ActionType(IEnum):
    ACTION_1 = "action_1"
    ACTION_2 = "action_2"


