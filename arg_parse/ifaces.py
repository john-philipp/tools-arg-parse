from abc import ABC, abstractmethod


class IEnum:
    @classmethod
    def choices(cls):
        return [y for x, y in cls.__dict__.items() if not x.startswith("_") and not isinstance(y, classmethod)]


class IParser(ABC):
    @abstractmethod
    def add_args(self, parent_parser):
        raise NotImplementedError()
