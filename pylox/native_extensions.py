from LoxCallable import LoxCallable
import time


class NativeClock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments):
        return time.time()

    def __repr__(self) -> str:
        return "<native fn>"
