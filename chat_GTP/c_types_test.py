import ctypes

# 載入 Pico SDK 的 C 函數庫
qspi = ctypes.CDLL("libpicoqspi.so")

# 初始化 QSPI
qspi.qspi_init_default()

# 進行 QSPI 讀取
read_data = bytearray(4)
qspi.qspi_inst_read_blocking(qspi.qspi_default, 0, read_data, len(read_data))

# 輸出讀取的數據
print("Read data:", read_data)


'''
try this to open the function of using external SPI flash 



'''