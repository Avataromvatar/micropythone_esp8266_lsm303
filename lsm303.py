import machine

import sfcp
import bins_sfcp_header

## https://github.com/jackw01/lsm303-python/blob/master/lsm303/__init__.py
LSM303_ADDRESS_ACCEL = 0x19 # 0011001x
LSM303_REGISTER_ACCEL_CTRL_REG1_A         = 0x20
LSM303_REGISTER_ACCEL_CTRL_REG2_A         = 0x21
LSM303_REGISTER_ACCEL_CTRL_REG3_A         = 0x22
LSM303_REGISTER_ACCEL_CTRL_REG4_A         = 0x23
LSM303_REGISTER_ACCEL_CTRL_REG5_A         = 0x24
LSM303_REGISTER_ACCEL_CTRL_REG6_A         = 0x25
LSM303_REGISTER_ACCEL_REFERENCE_A         = 0x26
LSM303_REGISTER_ACCEL_STATUS_REG_A        = 0x27
LSM303_REGISTER_ACCEL_OUT_X_L_A           = 0x28
LSM303_REGISTER_ACCEL_OUT_X_H_A           = 0x29
LSM303_REGISTER_ACCEL_OUT_Y_L_A           = 0x2A
LSM303_REGISTER_ACCEL_OUT_Y_H_A           = 0x2B
LSM303_REGISTER_ACCEL_OUT_Z_L_A           = 0x2C
LSM303_REGISTER_ACCEL_OUT_Z_H_A           = 0x2D
LSM303_REGISTER_ACCEL_FIFO_CTRL_REG_A     = 0x2E
LSM303_REGISTER_ACCEL_FIFO_SRC_REG_A      = 0x2F
LSM303_REGISTER_ACCEL_INT1_CFG_A          = 0x30
LSM303_REGISTER_ACCEL_INT1_SOURCE_A       = 0x31
LSM303_REGISTER_ACCEL_INT1_THS_A          = 0x32
LSM303_REGISTER_ACCEL_INT1_DURATION_A     = 0x33
LSM303_REGISTER_ACCEL_INT2_CFG_A          = 0x34
LSM303_REGISTER_ACCEL_INT2_SOURCE_A       = 0x35
LSM303_REGISTER_ACCEL_INT2_THS_A          = 0x36
LSM303_REGISTER_ACCEL_INT2_DURATION_A     = 0x37
LSM303_REGISTER_ACCEL_CLICK_CFG_A         = 0x38
LSM303_REGISTER_ACCEL_CLICK_SRC_A         = 0x39
LSM303_REGISTER_ACCEL_CLICK_THS_A         = 0x3A
LSM303_REGISTER_ACCEL_TIME_LIMIT_A        = 0x3B
LSM303_REGISTER_ACCEL_TIME_LATENCY_A      = 0x3C
LSM303_REGISTER_ACCEL_TIME_WINDOW_A       = 0x3D

LSM303_ADDRESS_MAG = 0x1E # 0011110x
LSM303_REGISTER_MAG_CRA_REG_M             = 0x00
LSM303_REGISTER_MAG_CRB_REG_M             = 0x01
LSM303_REGISTER_MAG_MR_REG_M              = 0x02
LSM303_REGISTER_MAG_OUT_X_H_M             = 0x03
LSM303_REGISTER_MAG_OUT_X_L_M             = 0x04
LSM303_REGISTER_MAG_OUT_Z_H_M             = 0x05
LSM303_REGISTER_MAG_OUT_Z_L_M             = 0x06
LSM303_REGISTER_MAG_OUT_Y_H_M             = 0x07
LSM303_REGISTER_MAG_OUT_Y_L_M             = 0x08
LSM303_REGISTER_MAG_SR_REG_Mg             = 0x09
LSM303_REGISTER_MAG_IRA_REG_M             = 0x0A
LSM303_REGISTER_MAG_IRB_REG_M             = 0x0B
LSM303_REGISTER_MAG_IRC_REG_M             = 0x0C
LSM303_REGISTER_MAG_TEMP_OUT_H_M          = 0x31
LSM303_REGISTER_MAG_TEMP_OUT_L_M          = 0x32

MAG_GAIN_1_3                              = 0x20 # +/- 1.3
MAG_GAIN_1_9                              = 0x40 # +/- 1.9
MAG_GAIN_2_5                              = 0x60 # +/- 2.5
MAG_GAIN_4_0                              = 0x80 # +/- 4.0
MAG_GAIN_4_7                              = 0xA0 # +/- 4.7
MAG_GAIN_5_6                              = 0xC0 # +/- 5.6
MAG_GAIN_8_1                              = 0xE0 # +/- 8.1

MAG_RATE_0_7                              = 0x00 # 0.75 H
MAG_RATE_1_5                              = 0x01 # 1.5 Hz
MAG_RATE_3_0                              = 0x62 # 3.0 Hz
MAG_RATE_7_5                              = 0x03 # 7.5 Hz
MAG_RATE_15                               = 0x04 # 15 Hz
MAG_RATE_30                               = 0x05 # 30 Hz
MAG_RATE_75                               = 0x06 # 75 Hz
MAG_RATE_220                              = 0x07 # 210 Hz

ACCEL_MS2_PER_LSB = 0.00980665 # meters/second^2 per least significant bit

GAUSS_TO_MICROTESLA = 100.0

class accel():
    def __init__(self, i2c):
        self.type = "LSM303"
        self.iic = i2c
        self.sfcp= sfcp.sfcp()
        # self.acReadAddr = 0x33
        # self.acWriteAddr = 0x32
        # self.maReadAddr = 0x3D
        # self.maWriteAddr = 0x3C
        self.acAddr = 0x19
        self.maAddr = 0x1E
        self.count=0
        self.iic.start()
        # Enable the accelerometer - all 3 channels
        
        self.iic.writeto(self.acAddr, bytearray([LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0b01110111]))
        self.iic.start()
        a = self.iic.readfrom_mem(self.acAddr, LSM303_REGISTER_ACCEL_CTRL_REG1_A, 1)
        print("Enable the accelerometer - all 3 channels ",a[0])
        self.iic.stop()
        self.set_acc_range(2)
        self.iic.start()
        print("On Magnitude Temp On 0b10000000 Freq 75Hz 0b00011000")
        self.iic.writeto(self.maAddr, bytearray([LSM303_REGISTER_MAG_MR_REG_M, 0b10011000]))
        self.iic.stop()
        self.iic.start()
        print("Set Magnitude Gain 1.9 ")
        self.set_mag_gain(MAG_GAIN_1_9)
        print("END INIT LSM303")
        self.iic.stop()

    def get_raw_values(self)-> []:
        self.iic.start()
        #in littel endian 12bit
        a = self.iic.readfrom_mem(self.acAddr, LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80, 6)
        # print(a[0],a[1],a[2],a[3],a[4],a[5])
        m = self.read_mag()
        t = self.iic.readfrom_mem(self.maAddr, 0x31, 2)
        c = []
        c.extend(a)
        c.extend(t)
        c.extend(m)
        self.iic.stop()
        return c
    def get_sfcp_message(self,is_response = 1)-> []:
        self.iic.start()
        #in littel endian 12bit
        a = self.iic.readfrom_mem(self.acAddr, LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80, 6)
        # print(a[0],a[1],a[2],a[3],a[4],a[5])
        m = self.read_mag()
        t = self.iic.readfrom_mem(self.maAddr, LSM303_REGISTER_MAG_TEMP_OUT_H_M, 2)
        self.iic.stop()
        msg = self.sfcp.init_message(bins_sfcp_header.BINS_MSG_TYPE,0,is_response)
        self.sfcp.add(msg,bins_sfcp_header.BINS_DATA_TYPE_COUNT,0,self.count)
        self.count+=1
        if self.count>=255:
            self.count=0
        self.sfcp.add(msg,bins_sfcp_header.BINS_DATA_TYPE_ACC_X,1,a[0]|(a[1]<<8))
        self.sfcp.add(msg,bins_sfcp_header.BINS_DATA_TYPE_ACC_Y,1,a[2]|(a[3]<<8))
        self.sfcp.add(msg,bins_sfcp_header.BINS_DATA_TYPE_ACC_Z,1,a[4]|(a[5]<<8))
        self.sfcp.add(msg,bins_sfcp_header.BINS_DATA_TYPE_MAG_X,1,m[1]|(m[0]<<8))
        self.sfcp.add(msg,bins_sfcp_header.BINS_DATA_TYPE_MAG_Y,1,m[3]|(m[2]<<8))
        self.sfcp.add(msg,bins_sfcp_header.BINS_DATA_TYPE_MAG_Z,1,m[5]|(m[4]<<8))
        self.sfcp.add(msg,bins_sfcp_header.BINS_DATA_TYPE_TEMP,1,t[1]|(t[0]<<8))
        # c = []
        # c.extend(a)
        # c.extend(t)
        # c.extend(m)
        
        return msg

    # def get_ints(self):
    #     b = self.get_raw_values()
    #     c = []
    #     c.count
    #     for i in b:
    #         c.append(i)
    #     return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        raw_ints.insert(0,self.count)
        self.count= self.count+1
        if self.count>=255:
            self.count=0
        return bytes(raw_ints)

    def set_mag_gain(self, gain):
        #'Set magnetometer gain'
        self._gain = gain
        if gain == MAG_GAIN_1_3:
            self._lsb_per_gauss_xy = 1100
            self._lsb_per_gauss_z = 980
        elif gain == MAG_GAIN_1_9:
            self._lsb_per_gauss_xy = 855
            self._lsb_per_gauss_z = 760
        elif gain == MAG_GAIN_2_5:
            self._lsb_per_gauss_xy = 670
            self._lsb_per_gauss_z = 600
        elif gain == MAG_GAIN_4_0:
            self._lsb_per_gauss_xy = 450
            self._lsb_per_gauss_z = 400
        elif gain == MAG_GAIN_4_7:
            self._lsb_per_gauss_xy = 400
            self._lsb_per_gauss_z = 355
        elif gain == MAG_GAIN_5_6:
            self._lsb_per_gauss_xy = 330
            self._lsb_per_gauss_z = 295
        elif gain == MAG_GAIN_8_1:
            self._lsb_per_gauss_xy = 230
            self._lsb_per_gauss_z = 205
        self.iic.writeto(self.maAddr, bytearray([LSM303_REGISTER_MAG_CRB_REG_M, self._gain]))
        # self._bus.write_i2c_block_data(LSM303_ADDRESS_MAG,
        #                                LSM303_REGISTER_MAG_CRB_REG_M,
        #                                [self._gain])
    def set_acc_range(self,range):
        s = 0b00001000
        if range == 4:
            s = 0b00001000|0b00010000 #+-4g
        elif range == 8:
            s = 0b00001000|0b00100000 #+-8g    
        elif range == 16:
            s = 0b00001000|0b00110000 #+-16g        
        self.iic.start()
        # Select hi-res (12-bit)
        print("Select hi-res (12-bit) Range:", range)

        self.iic.writeto(self.acAddr, bytearray([LSM303_REGISTER_ACCEL_CTRL_REG4_A, s]))
        self.iic.stop()

    def set_mag_rate(self, rate):
        #'Set magnetometer rate'
        self.iic.writeto(self.maAddr, bytearray([LSM303_REGISTER_MAG_CRA_REG_M, (rate & 0x07) << 2]))
        # self._bus.write_i2c_block_data(LSM303_ADDRESS_MAG,
        #                                LSM303_REGISTER_MAG_CRA_REG_M,
        #                                [(rate & 0x07) << 2])

    def read_mag(self):
        #'Read raw magnetic field in microtesla'
        # Read as signed 16-bit big endian values
        mag_bytes = self.iic.readfrom_mem(self.maAddr, LSM303_REGISTER_MAG_OUT_X_H_M, 6)
        return mag_bytes
        # mag_bytes = self._bus.read_i2c_block_data(LSM303_ADDRESS_MAG,
        #                                           LSM303_REGISTER_MAG_OUT_X_H_M,
        #                                           6)
        # mag_raw = struct.unpack('>hhh', bytearray(mag_bytes))
        magX = int(self.bytes_toint(mag_bytes[0],mag_bytes[1])/ self._lsb_per_gauss_xy * GAUSS_TO_MICROTESLA)
        magZ = int(self.bytes_toint(mag_bytes[2],mag_bytes[3])/ self._lsb_per_gauss_z * GAUSS_TO_MICROTESLA)
        magY = int(self.bytes_toint(mag_bytes[4],mag_bytes[5])/ self._lsb_per_gauss_xy * GAUSS_TO_MICROTESLA)
        return bytes([(magX>>8)&0xFF,magX&0xFF,(magZ>>8)&0xFF,magZ&0xFF,(magY>>8)&0xFF,magY&0xFF])
        # return (
        #     mag_raw[0] / self._lsb_per_gauss_xy * GAUSS_TO_MICROTESLA,
        #     mag_raw[2] / self._lsb_per_gauss_xy * GAUSS_TO_MICROTESLA,
        #     mag_raw[1] / self._lsb_per_gauss_z * GAUSS_TO_MICROTESLA,
        # )  

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)