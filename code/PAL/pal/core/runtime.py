import copy
import datetime
from typing import Any, Dict
import dateutil.relativedelta


class GenericRuntime:
    GLOBAL_DICT = {}
    LOCAL_DICT = None
    HEADERS = []

    def __init__(self):
        self._global_vars = copy.copy(self.GLOBAL_DICT)
        self._local_vars = copy.copy(
            self.LOCAL_DICT) if self.LOCAL_DICT else None

        for c in self.HEADERS:
            self.exec_code(c)

    def exec_code(self, code_piece: str) -> None:
        print(code_piece)
        exec(code_piece, self._global_vars)

    def eval_code(self, expr: str) -> Any:
        print(expr)
        return eval(expr, self._global_vars)

    def inject(self, var_dict: Dict[str, Any]) -> None:
        for k, v in var_dict.items():
            self._global_vars[k] = v

    @property
    def answer(self):
        return self._global_vars['answer']


class DateRuntime(GenericRuntime):
    GLOBAL_DICT = {
        'datetime': datetime.datetime,
        'timedelta': dateutil.relativedelta.relativedelta,
        'relativedelta': dateutil.relativedelta.relativedelta
    }


class CustomDict(dict):
    def __iter__(self):
        return list(super().__iter__()).__iter__()


class ColorObjectRuntime(GenericRuntime):
    GLOBAL_DICT = {'dict': CustomDict}
