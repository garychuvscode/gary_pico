"""
this file used to identify the type of board
since there are few type of board may be used for application
1. pcio original
2. pcio w original
3. YD-2040
4. T-PicoC3

these are different type of pico main board, need to be separated
since the hardware configuration are not the same

hardware configuration refer to the one note file
"""

# fmt: off
# the device will identify base on the index of above:
device_index = 3

# firmware version will need to think about how to implement
# may be in other file call update log
