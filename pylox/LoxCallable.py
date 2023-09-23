import abc


class LoxCallable(abc.ABC):
    @abc.abstractmethod
    def arity(self) -> int:
        """returns arity (number of arguments) of the function"""

    @abc.abstractmethod
    def call(self, interpreter, arguments: list):
        """calls function in interpreter"""
