import machine
from machine import Pin

# fmt: off
# PWM settings
freq0 = 10000000
duty_u16_0 = 32765
pwm0_pin = 8
pwm1_pin = 0


# # pwm0 = machine.PWM(Pin(8), freq=freq0, duty_u16=duty_u16_0)
# pwm0 = machine.PWM(Pin(8), freq=freq0, duty_u16=50)

# while 1:
#     # a = float(input())
#     # a = a / 65536
#     # pwm0.duty_u16(a)

#     # print(f"input frequency settings")
#     # freq = int(input())
#     # print(f"frequency set to {freq}")
#     # pwm0.freq(freq)

#     print(
#         f"input duty settings is {pwm0.duty_u16()}, /65535 is {float(pwm0.duty_u16())/65535} and % is {int(float(pwm0.duty_u16())/65535*100)}"
#     )
#     print(
#         f"pwm_d is {pwm0.duty_u16()}, result is {float(pwm0.duty_u16())/65535}, percentage: {pwm0.duty_u16()/65535*100}"
#     )
#     a = input()
#     b = float(a) / 100
#     c = b * 65535

#     duty = int(c)
#     print(f"duty set to {duty}, with {a}%, {b} after / 100, {c} is the result")
#     pwm0.duty_u16(duty)

#     if a == 0:
#         pwm0.deinit()
#         pass
#     # else:
#     #     pwm0.init(freq=freq0, duty_u16=duty_u16_0)

freq_set = 1000000


# def pwm_ctrl(freq0=None, duty0=50, type0=0, ch0=0, dis0=0):
#     """
#     duty is either % or duration_ns, depends on type
#     type: 0- duty in %, 1- duration_ns
#     if no freq setting, freq set to default
#     """

#     if freq0 == None:
#         # use default setting for frequency
#         freq0 = freq_set
#     else:
#         freq0 = int(freq0)

#     if type0 == 0:
#         # duty in %
#         duty_nor = float(duty0) / 100
#         duty_res = int(duty_nor * 65535)
#         pass
#     else:
#         # duty in ns, no need for process
#         duty_res = int(duty0)
#         pass

#     pwm0 = machine.PWM(Pin(pwm0_pin), freq=freq_set, duty_u16=0)
#     pwm1 = machine.PWM(Pin(pwm1_pin), freq=freq_set, duty_u16=0)

#     if dis0 != 0:
#         # define PWM mode
#         if ch0 == 0:
#             # active pwm0
#             if type0 == 0:
#                 # % mode
#                 pwm0 = machine.PWM(Pin(pwm0_pin), freq=freq0, duty_u16=duty_res)
#             else:
#                 # ns mode
#                 pwm0 = machine.PWM(Pin(pwm0_pin), freq=freq0, duty_ns=duty_res)
#         elif ch0 == 1:
#             # active pwm0
#             if type0 == 0:
#                 # % mode
#                 pwm1 = machine.PWM(Pin(pwm1_pin), freq=freq0, duty_u16=duty_res)
#             else:
#                 # ns mode
#                 pwm1 = machine.PWM(Pin(pwm1_pin), freq=freq0, duty_ns=duty_res)
#     else:
#         # no need to use deinit() to turn off, only set duty to 0 is ok
#         if ch0 == 0:
#             # pwm0 off
#             pwm0.deinit()
#         elif ch0 == 1:
#             # pwm0 off
#             pwm1.deinit()

pwm0 = machine.PWM(Pin(pwm0_pin), freq=freq_set, duty_u16=0)
pwm1 = machine.PWM(Pin(pwm1_pin), freq=freq_set, duty_u16=0)

def pwm_ctrl(freq0=None, duty0=0, type0=0, ch0=0):
    """
    duty is either % or duration_ns, depends on type
    type: 0- duty in %, 1- duration_ns
    if no freq setting, freq set to default
    set duty to 0 to disable
    """

    if freq0 == None:
        # use default setting for frequency
        freq0 = freq_set
    else:
        freq0 = int(freq0)

    if type0 == 0:
        # duty in %
        duty_nor = float(duty0) / 100
        duty_res = int(duty_nor * 65535)
        pass
    else:
        # duty in ns, no need for process
        duty_res = int(duty0)
        pass

    if ch0 == 0:
        # active pwm0
        if type0 == 0:
            # % mode
            pwm0 = machine.PWM(Pin(pwm0_pin), freq=freq0, duty_u16=duty_res)
        else:
            # ns mode
            pwm0 = machine.PWM(Pin(pwm0_pin), freq=freq0, duty_ns=duty_res)
    elif ch0 == 1:
        # active pwm0
        if type0 == 0:
            # % mode
            pwm1 = machine.PWM(Pin(pwm1_pin), freq=freq0, duty_u16=duty_res)
        else:
            # ns mode
            pwm1 = machine.PWM(Pin(pwm1_pin), freq=freq0, duty_ns=duty_res)


while 1:
    print(f"pwm controll setting, enter: duty; type; ch; dis")
    x = input()
    x_list = x.split(";")
    # duty; type; ch; dis
    print(f"the input is: {x_list}")
    # pwm_ctrl(
    #     freq0=int(x_list[0]),
    #     duty0=int(x_list[1]),
    #     type0=int(x_list[2]),
    #     ch0=int(x_list[3]),
    # )
    pwm_ctrl(
        freq0=int(int(x_list[0])*100000),
        duty0=int(x_list[1]),
        type0=1,
        ch0=0,
    )
    pass
