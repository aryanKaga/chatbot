from typing import Callable, List, Tuple, Any
from cache import check_similarity
class Pipeline:

    def __init__(self, funcs: List[Tuple[Callable, Any]] = []):
        self.funcs = funcs

    def append(self, funcs: List[Tuple[Callable, Any]]):
        self.funcs += funcs

    def stream(self):
        for func, args in self.funcs:
            if args is None:
                output = func()
            elif isinstance(args, tuple):
                output = func(*args)
            elif isinstance(args, dict):
                output = func(**args)
            else:
                output = func(args)
            print(output)


    