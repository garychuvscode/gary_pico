"""
this file move the main to below and renamed to sub_main

to prevent other's get the main code directly from load
the project of PICO

"""

import uos
import utime

# the original will be main.py
"""
for the general situation, just copy the main to pico, can
also backup the source code

try to move the main program to 'grace' directory under flash (/)
and use the module path to import program
"""

try:
    # create new directory 'grace' under flash
    try:
        space = uos.statvfs("/flash")
        total_space = space[0] * space[2]
        free_space = space[0] * space[3]
        print(f"Total Space: {total_space} bytes, Free Space: {free_space} bytes")
    except OSError as e:
        print(f"Error checking space: {e}")
    uos.mkdir("/grace")
    pass

except OSError as e:
    print(f"Error creat dir: {e}")
    pass

try:
    # list and check if create ok
    uos.listdir("/")
    pass

except OSError as e:
    print(f"Error listing files: {e}")
    pass

try:
    old_name0 = "//sub_main.py"
    new_name0 = "//grace/sub_main.py"
    uos.rename(old_name0, new_name0)
    pass

except OSError as e:
    print(f"Error moving file: {e}")
    pass

try:
    # list and check if create ok
    print(f'list down flash "//grace" ')
    uos.listdir("//grace")
    pass

except OSError as e:
    print(f"Error creat dir: {e}")
    pass


try:
    # list and check if create ok
    print(f' the stuff under flash(/) : {uos.listdir("/")}\n')
    print(f'and the file under grace: {uos.listdir("//grace")}')
    pass

except OSError as e:
    print(f"Error creat dir: {e}")
    pass

print(f"process finished")
