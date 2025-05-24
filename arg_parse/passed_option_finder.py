import argparse


class PassedOptionFinder:

    # TODO need to include mode_action_{all_dests} in option_paths.
    def __init__(self, arg_parser):
        self._arg_parser = arg_parser
        self._sub_parser = arg_parser
        self._current_destination = None

        # Map all known flags (long and short) to their destination.
        self._option_to_action = {}
        self._dest_to_long_option = {}

    def nest_into_parser(self, *destinations):
        for destination in destinations:
            self._sub_parser = self._get_sub_parser(self._sub_parser, destination)
            self._current_destination = destination

    def find_long_options_passed(self, passed_args):
        for action in self._sub_parser._actions:
            self._collect_possible_options(action, self._option_to_action, self._dest_to_long_option)

        if self._current_destination is None:
            action_index = 0
        else:
            try:
                # Start parsing argv from the point after the action.
                action_index = passed_args.index(self._current_destination)
            except ValueError:
                raise ValueError(f"Action '{self._current_destination}' not found in argv.")

        relevant_args = passed_args[action_index + 1:]
        return self._collect_long_options_passed(relevant_args)

    def _collect_long_options_passed(self, args):
        long_options_passed = {}
        for i, arg in enumerate(args):
            if arg.startswith('--') or arg.startswith('-'):
                # Three cases:
                #  1. -[-]f[lag]={value}
                #  2. -[-]f[lag] (stand-alone boolean)
                #  3. -[-]f[lag] {value}
                if '=' in arg:
                    option_string, option_value = arg.split('=', 1)
                else:
                    option_string = arg
                    option_value = self._get_arg_value(args, i + 1)

                action = self._option_to_action.get(option_string)
                # Unknown option, skip.
                if not action:
                    continue

                long_option_string = next(self._option_string_gen(action), option_string)
                long_option_name = long_option_string.lstrip("-").replace("-", "_")
                long_options_passed[long_option_name] = option_value

        return long_options_passed

    def _collect_possible_options(self, action, option_to_action, dest_to_long_option):
        if not action.option_strings:
            return
        for option_string in action.option_strings:
            option_to_action[option_string] = action
        long_option = next(self._option_string_gen(action), None)
        if long_option:
            dest_to_long_option[action.dest] = long_option

    def _get_sub_parser(self, parser_, dest):
        # Not. This currently assumes a single sub-parser.
        action = next(self._action_gen(parser_), None)
        if not action:
            raise ValueError("Top-level parser has no subparsers (mode).")
        return action.choices[dest]

    def _get_arg_value(self, args, i):
        # Implicitly assumes next arg that isn't a flag is a value.
        # This may turn out to be wrong when working on args
        # for preceding actions.
        if not self._is_arg_flag(args, i):
            return True
        return args[i]

    @staticmethod
    def _is_arg_flag(args, i):
        return i < len(args) and not args[i].startswith('-')

    @staticmethod
    def _action_gen(parser):
        return (a for a in parser._actions if isinstance(a, argparse._SubParsersAction))

    @staticmethod
    def _option_string_gen(action):
        return (o for o in action.option_strings if o.startswith('--'))
