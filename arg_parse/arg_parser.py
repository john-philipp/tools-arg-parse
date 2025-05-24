import argparse

from arg_parse.ifaces import Args
from arg_parse.passed_option_finder import PassedOptionFinder


class ArgParser:

    class OptArgs:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    def __init__(
            self,
            args_cls: Args.__class__ = None,
            from_file_path=None,
            from_env_prefix=None):

        self._args_cls = args_cls
        self._from_file_path = from_file_path
        self._from_env_prefix = from_env_prefix

    def parse_args(self, parser: argparse.ArgumentParser, *args):

        parsed_args = parser.parse_args(args)
        if not self._args_cls:
            return parsed_args

        args_: Args = self._args_cls()
        args_.from_args(parsed_args)

        updated = []
        if self._from_file_path:
            updated += args_.from_file(self._from_file_path)
        if self._from_env_prefix:
            updated += args_.from_env(self._from_env_prefix)

        if updated:
            # We override from actually passed args, if we read from file and/or env.
            passed_option_finder = PassedOptionFinder(parser)

            # TODO: get rid of assumption mode/action? Or define it.
            passed_option_finder.nest_into_parser(parsed_args.mode, parsed_args.action)
            passed_args = passed_option_finder.find_long_options_passed(args)
            args_.from_args(passed_args)

        return args_

