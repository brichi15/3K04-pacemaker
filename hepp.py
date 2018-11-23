import serial
import struct

Par_File = open("Parameters.txt","r")
Parameters = Par_File.readlines()
Par_File.close()

def Load_Values(Username):
    user_file = open('userdata/'+Username,"r")
    p = user_file.readlines()
    a = []
    b = []
    byte_b = []
    byte_length = [4,1,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,1,1,1,1,1,1]
    

    for i in range(0,len(Parameters)):
        a.append(p[i][p[i].find(": ")+2:-1])
        print(p[i][p[i].find(": ")+2:-1])

    for i in a:
        if i.find('.')>0:
            b.append(int(round(float(i),1)*1000))
        elif i == 'OFF':
            b.append(0)
        elif i == 'ON': 
            b.append(1)
        elif i.find('High')>=0 or i.find('Low')>=0 or i.find('Med')>=0:
            if i == "V-Low": b.append(1)
            if i == "V-Low": b.append(2)
            if i == "Low": b.append(3)
            if i == "Med-Low": b.append(4)
            if i == "Med": b.append(5)
            if i == "Med-High": b.append(6)
            if i == "High": b.append(7)
            if i == "V-High": b.append(8)
        elif i == "OFF": b.append(0) 
        elif i == "AAT": b.append(1) 
        elif i == "VVT": b.append(2)
        elif i == "AOO": b.append(3)
        elif i == "AAI": b.append(4)
        elif i == "VOO": b.append(5)
        elif i == "VVI": b.append(6)
        elif i == "VDD": b.append(7)
        elif i == "DOO": b.append(8)
        elif i == "DDI": b.append(9)
        elif i == "DDD": b.append(10)
        elif i == "AOOR": b.append(11)
        elif i == "AAIR": b.append(12)
        elif i == "VOOR": b.append(13)
        elif i == "VVIR": b.append(14)
        elif i == "VDDR": b.append(15)
        elif i == "DOOR": b.append(16)
        elif i == "DDIR": b.append(17)
        elif i == "DDDR": b.append(18)
        else:
            try:
                b.append(int(i))
            except ValueError:
                b.append(i)

    for i in range(0,26):
        if b[i]>=0:
            byte_b.append(b[i].to_bytes(byte_length[i], byteorder='big'))
        elif b[i]<0:
            byte_b.append(b[i].to_bytes(byte_length[i], byteorder='big',signed=True))



    print(byte_b)
    print(b)
    print(len(a))


Load_Values("oscar")

##ser = serial.Serial('COM6', baudrate=115200)
##print(ser.name)
##cmd = b'\x16\x55'
##
##ser.write(cmd)
##for i in byte_b:
##    ser.write(i)
##
##ser.write(bytes(1))
##ser.close()
