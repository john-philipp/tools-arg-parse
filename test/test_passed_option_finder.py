import argparse
import unittest

from arg_parse.passed_option_finder import PassedOptionFinder


class _OptDef:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class TestPassedOptionFinder(unittest.TestCase):

    @staticmethod
    def _build_arg_parser(nest_level_and_options):
        parent_parser = argparse.ArgumentParser()
        arg_parser = parent_parser

        sub_parser_groups = {}

        for i, option_definition_wrapper in enumerate(nest_level_and_options):
            dest, mode, option_definitions = option_definition_wrapper
            sub_parser_group = sub_parser_groups.get(dest)
            if not sub_parser_group:
                sub_parser_group = arg_parser.add_subparsers(dest=dest)
                sub_parser_groups[dest] = sub_parser_group

            sub_parser = sub_parser_group.add_parser(mode)
            for option_definition in option_definitions:
                sub_parser.add_argument(*option_definition.args, **option_definition.kwargs)

            # We nest by default.
            arg_parser = sub_parser

        return parent_parser

    def _base_template_test(self, argv, expected, destinations, args_definitions=None):
        if not args_definitions:
            args_definitions=[
                ("mode", "build", []),
                ("action", "docker", [
                    _OptDef('-t', '--tag'),
                    _OptDef('-n', '--no-cache', action='store_true'),
                    _OptDef('-x', '--tag2'),
                ])
            ]
        arg_parser = self._build_arg_parser(args_definitions)
        passed_option_finder = PassedOptionFinder(arg_parser)
        passed_option_finder.nest_into_parser(*destinations)
        flags = passed_option_finder.find_long_options_passed(argv)
        self.assertEqual(flags, expected)

    def test_many_intermixed_options(self):
        self._base_template_test(
            ['build', 'docker', '--tag', 'latest', '-n', '--tag2=123'],
            {'--tag': 'latest', '--no-cache': True, '--tag2': '123'},
            ["build", "docker"])

    def test_single_long_option(self):
        self._base_template_test(
            ["build", "--tag", "some_tag"],
            {"--tag": "some_tag"},
            ["build"],
            args_definitions=[
                ("mode", "build", [_OptDef("-t", "--tag")])
            ])

    def test_single_short_option(self):
        self._base_template_test(
            ["build", "-t", "some_tag"],
            {"--tag": "some_tag"},
            ["build"],
            args_definitions=[
                ("mode", "build", [_OptDef("-t", "--tag")])
            ])

    def test_standalone_boolean_1(self):
        self._base_template_test(
            ["build", "-n"],
            {"--no-cache": True},
            ["build"],
            args_definitions=[
                ("mode", "build", [_OptDef("-n", "--no-cache", action="store_true")])
            ])

    def test_standalone_boolean_2(self):
        self._base_template_test(
            ["build", "-n", "-t", "some_tag"],
            {"--no-cache": True, "--tag": "some_tag"},
            ["build"],
            args_definitions=[
                ("mode", "build", [
                    _OptDef("-t", "--tag"),
                    _OptDef("-n", "--no-cache", action="store_true")
                ])
            ])

    def test_skip_next(self):
        self._base_template_test(
            ["build", "-t=some_tag", "-n"],
            {"--no-cache": True, "--tag": "some_tag"},
            ["build"],
            args_definitions=[
                ("mode", "build", [
                    _OptDef("-t", "--tag"),
                    _OptDef("-n", "--no-cache", action="store_true")
                ])
            ])

    def test_multiple_long_options_and_boolean(self):
        self._base_template_test(
            ["deploy", "--region=us-west-1", "--force"],
            {"--region": "us-west-1", "--force": True},
            ["deploy"],
            args_definitions=[
                ("mode", "deploy", [
                    _OptDef("--region", type=str),
                    _OptDef("--force", action="store_true")
                ])
            ])

    def test_action_not_in_argv_raises(self):
        with self.assertRaises(ValueError) as ctx:
            self._base_template_test(
                ["deploy", "--region", "us-east-1"],
                {},  # Doesn't matter
                ["missing"],
                args_definitions=[
                    ("mode", "missing", [_OptDef("--region")])
                ])
        self.assertIn("Action 'missing' not found in argv.", str(ctx.exception))

    def test_unknown_option_is_skipped(self):
        self._base_template_test(
            ["build", "--unknown", "value", "--tag", "v1.0"],
            {"--tag": "v1.0"},  # --unknown is ignored
            ["build"],
            args_definitions=[
                ("mode", "build", [_OptDef("--tag")])
            ])

    def test_get_sub_parser_raises_when_none(self):
        parser = argparse.ArgumentParser()
        finder = PassedOptionFinder(parser)
        with self.assertRaises(ValueError) as ctx:
            finder.nest_into_parser("noop")
        self.assertIn("Top-level parser has no subparsers", str(ctx.exception))

    def test_short_option_only_does_not_map_long(self):
        self._base_template_test(
            ["build", "-x", "value"],
            {"-x": "value"},
            ["build"],
            args_definitions=[
                ("mode", "build", [_OptDef("-x")])  # No --long form
            ])

    def test_no_arguments_provided(self):
        self._base_template_test(
            ["build"],
            {},  # No flags
            ["build"],
            args_definitions=[
                ("mode", "build", [_OptDef("--tag")])
            ])
