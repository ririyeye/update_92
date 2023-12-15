#!/usr/bin/python3


import sys
import pyvisa


def setwave(my_instrument):
    print(my_instrument.query('*IDN?'))
    my_instrument.write('*RST')

    """ALC关闭/开启（ALC关闭）"""
    my_instrument.write(':POWer:ALC:STATe OFF')
    print(my_instrument.query(':POWer:ALC:STATe?'))

    """设置波形和采样率"""
    my_instrument.write(':RADio:ARB:WAVeform "WFM1:WAVE_500_NEW"')
    print(my_instrument.query(':RADio:ARB:WAVeform?'))
    my_instrument.write(':RADio:ARB ON')
    print(my_instrument.query(':RADio:ARB?'))

    my_instrument.write(':RAD:ARB:SCL:RATE 2.240000E+7 Hz')
    print(my_instrument.query(':RAD:ARB:SCL:RATE?'))

    """设置RF开启、关闭（开启RF）"""
    my_instrument.write(':OUTPut ON')
    print(my_instrument.query(':OUTPut?'))

def config_freq(my_instrument , freq):
    """设置测试频点（以5880Mhz为例）"""
    my_instrument.write(':FREQ ' + str(freq))
    print(my_instrument.query(':FREQ?'))

def config_spec(my_instrument , spec):
    """设置spec（单位DB，Spec=-100dB时）"""
    my_instrument.write(':POWer ' + str(spec))
    print(my_instrument.query(':POWer?'))


if __name__ == "__main__":

    freq = 2480
    spec = -70

    if len(sys.argv) > 2:
        freq = int(sys.argv[1])
        spec = int(sys.argv[2])   
    print("try set {:d}Mhz with spec = {:d}dbm".format(freq , spec))


    rm = pyvisa.ResourceManager()
    source_list = rm.list_resources()
    print(source_list)


    instru = rm.open_resource(source_list[0])
    print('connect to INSTR success!')

    setwave(instru)
    config_freq(instru , freq * 1000 * 1000)
    config_spec(instru , spec)