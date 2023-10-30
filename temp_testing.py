import rp2
from machine import Pin


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)[0]
    # nop()[31]
    # nop()[31]
    # nop()[31]
    # nop()[31]
    set(pins, 0)[0]
    # nop()[31]
    # nop()[31]
    # nop()[31]
    # nop()[31]
    wrap()


sm = rp2.StateMachine(0, blink, freq=50000000, set_base=Pin(0))
sm.active(1)
