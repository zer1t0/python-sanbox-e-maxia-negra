import sys
import ast
from ctypes import pythonapi, POINTER, py_object


### block functions

blocked_functions = ["open"]

def block_functions(code_string):
    tree = compile(code_string, "input.py", "exec", flags=ast.PyCF_ONLY_AST)
    # print(ast.dump(tree, indent=4))
    for el in ast.walk(tree):
        if isinstance(el, ast.Call) and isinstance(el.func, ast.Name):
            func_name = el.func.id
            if func_name in blocked_functions:
                raise ValueError("Found blacklisted function: {}".format(el.func.id))

def block_words(code_string):
    for keyword in blocked_functions:
        if keyword in code_string:
            raise ValueError("Found blacklisted keyword: {}".format(keyword))


#### Clear builtins

def clear_builtins():
    main = sys.modules["__main__"].__dict__
    builtins = main["__builtins__"].__dict__

    builtin_blacklist = ["open"]
    # builtin_blacklist.append("__loader__")

    for builtin in list(builtins.keys()):
        if builtin in builtin_blacklist:
            del builtins[builtin]

clear_builtins()

#### Whitelist imports

module_whitelist = ["re"]

def _safe_import(orig_import, whitelist):
    def safe_import(module_name, *args, **kwargs):

        if module_name not in set(whitelist):
            raise ImportError("Import blocked: {}".format(module_name))

        return orig_import(module_name, *args, **kwargs)

    return safe_import


def whitelist_imports():
    main = sys.modules["__main__"].__dict__
    orig_builtins = main["__builtins__"].__dict__

    orig_builtins["__import__"] = _safe_import(
        __import__,
        module_whitelist
    )

whitelist_imports()


#### remove __bases__ and __subclasses__

_get_dict = pythonapi._PyObject_GetDictPtr
_get_dict.restype = POINTER(py_object)
_get_dict.argtypes = [py_object]
del pythonapi, POINTER, py_object

def dictionary_of(ob):
    dptr = _get_dict(ob)
    return dptr.contents.value

def remove_super_and_sub_classes():
    type_dict = dictionary_of(type)
    del type_dict["__bases__"]
    del type_dict["__base__"]
    del type_dict["__subclasses__"]

remove_super_and_sub_classes()


class Sandbox():

    def __init__(self, globals=None, locals=None):
        self.globals = globals or {}
        self.locals = locals or {}

    def execute(self, code_string):
        # block_functions(code_string)
        # block_words(code_string)
        exec(code_string, self.globals, self.locals)

