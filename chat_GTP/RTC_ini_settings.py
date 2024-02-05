import machine
# 240204 RTC object is in machine
from machine import RTC

rtc = RTC()

# init will be set during definition of object
# rtc.init()

# 設定時間，這裡以2022年2月3日 12:34:56為例
rtc.datetime((2022, 2, 3, 0, 12, 34, 56, 0))

# 讀取時間
year, month, day, weekday, hours, minutes, seconds, subseconds = rtc.datetime()

print("Current time: {}-{}-{} {}:{}:{}".format(year, month, day, hours, minutes, seconds))
