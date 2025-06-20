import os
import logging
from abc import ABC, abstractmethod

from arg_parse.yaml.jinja_yaml_loader import JinjaYamlLoader


log = logging.getLogger(__name__)


class IEnum:
    @classmethod
    def valid(cls, value):
        return value in cls.choices()

    @classmethod
    def choices(cls):
        return [y for x, y in cls.__dict__.items() if not x.startswith("_") and not isinstance(y, classmethod)]


class IParserDef(ABC):
    @abstractmethod
    def register_args(self, parent_parser):
        raise NotImplementedError()


def snake_to_camel(snake_str):
    return ''.join(x.capitalize() for x in snake_str.split("_"))


VALID_VALUES_TRUE = ["1", "true", "True", "TRUE", "y", "yes", "Yes", "YES"]
VALID_VALUES_FALSE = ["0", "false", "False", "FALSE", "n", "no", "No", "NO", ""]


def convert_to_bool(source_value, log_error=None):
    if isinstance(source_value, bool):
        return source_value
    if source_value in VALID_VALUES_FALSE:
        return False
    elif source_value in VALID_VALUES_TRUE:
        return True
    else:
        if log_error:
            log_error(f"Couldn't convert to boolean: {source_value} type={type(source_value)}")
            log_error(f"Allowed for 'True': {VALID_VALUES_TRUE}")
            log_error(f"Allowed for 'False': {VALID_VALUES_FALSE}")
        raise ValueError("Failed conversion to boolean.")


class Origin(IEnum):
    DEFAULT = "default"
    ARGS = "args"
    FILE = "file"
    ENV = "env"


class Args(ABC):
    def __init__(self, calling_globals):
        self._validate = False
        self._calling_globals = calling_globals
        self._validate = True
        self._origin = {}

    @staticmethod
    def _convert(value, new_value):
        if isinstance(value, bool) and isinstance(new_value, str):
            new_value = convert_to_bool(new_value)
        elif isinstance(value, (float, int)) and isinstance(new_value, str):
            new_value = type(value)(new_value)
        return new_value

    def map_origin(self, from_value: Origin, to_value: Origin):
        self._origin = {x: to_value if y == from_value else y for x, y in self._origin.items()}

    def _visible_attrs_gen(self):
        return ((x, y) for x, y in self.__dict__.items() if not x.startswith("_"))

    def validate(self):
        for attr_name, attr_value in self._visible_attrs_gen():
            if attr_value is None:
                # Allow for default None.
                continue
            enum_cls_name = snake_to_camel(attr_name)
            if enum_cls_name not in self._calling_globals:
                continue
            enum_cls = self._calling_globals[enum_cls_name]
            if not isinstance(enum_cls(), IEnum):
                raise ValueError(
                    f"Attribute {attr_name} has class {enum_cls_name} associated, which isn't an IEnum.")
            if not enum_cls.valid(attr_value):
                raise ValueError(
                    f"Unknown {attr_name} = {attr_value}. Valid: {enum_cls.choices()}. Use enum: {enum_cls_name}")

    def from_file(self, config_file_path, **bindings):
        changed = False
        updated_attrs = []
        if config_file_path:
            if not config_file_path.endswith(".yaml") and not config_file_path.endswith(".yml"):
                raise ValueError(f"Require a YAML file: {config_file_path}")
            loaded_data = JinjaYamlLoader(config_file_path, dict).load(**bindings)
            for attr_name, attr_value in self._visible_attrs_gen():
                if attr_name in loaded_data:
                    new_attr_value = loaded_data[attr_name]
                    if attr_value != new_attr_value:
                        self.__dict__[attr_name] = new_attr_value
                        updated_attrs.append(attr_name)
                        self._origin[attr_name] = Origin.FILE
                        changed = True
        if changed:
            self.validate()
        updated_attrs.sort()
        return updated_attrs

    def from_env(self, env_var_prefix=None):
        changed = False
        updated_attrs = []
        for attr_name, attr_value in self._visible_attrs_gen():
            try:
                env_var = self._as_env_var(attr_name, env_var_prefix)
                if env_var in os.environ:
                    new_attr_value = os.environ[env_var]
                    if attr_value is not None:
                        new_attr_value = self._convert(attr_value, new_attr_value)
                    if attr_value != new_attr_value:
                        self.__dict__[attr_name] = new_attr_value
                        updated_attrs.append(attr_name)
                        self._origin[attr_name] = Origin.ENV
                        changed = True
            except TypeError as ex:
                log.error(f"Error when handling: key={attr_name} value={attr_value}")
                raise ex
        if changed:
            self.validate()
        updated_attrs.sort()
        return updated_attrs

    def from_args(self, args):
        changed = False
        updated_attrs = []
        if args:
            if isinstance(args, dict):
                # Shorthand to turn into object.
                args = type("_T", (), args)()
            for attr_name, attr_value in self._visible_attrs_gen():
                try:
                    if hasattr(args, attr_name):
                        new_attr_value = getattr(args, attr_name)
                        if attr_value is not None:
                            new_attr_value = self._convert(attr_value, new_attr_value)
                        if attr_value != new_attr_value:
                            setattr(self, attr_name, new_attr_value)
                            updated_attrs.append(attr_name)
                            changed = True
                        self._origin[attr_name] = Origin.ARGS
                except TypeError as ex:
                    log.error(f"Error when handling: key={attr_name} value={attr_value}")
                    raise ex
        if changed:
            self.validate()
        updated_attrs.sort()
        return updated_attrs

    @staticmethod
    def _as_env_var(config_attr, env_var_prefix=None):
        env_var = config_attr.upper()
        if not env_var_prefix:
            return env_var
        return f"{env_var_prefix}_{env_var}"

    def log(self):
        for attr_name, attr_value in self._visible_attrs_gen():
            log.warning(f"args.{attr_name:20} = {attr_value.__str__():20} "
                        f"(from {self._origin.get(attr_name, Origin.DEFAULT):4})")
