import serial
import struct
import time

Par_File = open("Parameters.txt","r")
Parameters = Par_File.readlines()
Par_File.close()

def Load_Values(Username):
    user_file = open('userdata/'+Username,"r")
    p = user_file.readlines()
    a = []
    b = []
    byte_b = []
    byte_length = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    

    for i in range(0,len(Parameters)):
        a.append(p[i][p[i].find(": ")+2:-1])
        print(p[i][p[i].find(": ")+2:-1])
        
    

    for i in range(0,len(a)):
        if a[i].find('.')>0:
            b.append(int(round(float(a[i]),1)*1000))
        elif a[i] == 'OFF' and i > 0 :
            b.append(0)
        elif a[i] == 'ON': 
            b.append(1)
        elif a[i].find('High')>=0 or a[i].find('Low')>=0 or a[i].find('Med')>=0:
            if a[i] == "V-Low": b.append(1)
            if a[i] == "V-Low": b.append(2)
            if a[i] == "Low": b.append(3)
            if a[i] == "Med-Low": b.append(4)
            if a[i] == "Med": b.append(5)
            if a[i] == "Med-High": b.append(6)
            if a[i] == "High": b.append(7)
            if a[i] == "V-High": b.append(8)
        elif a[i] == "OFF" and i == 0: b.append(bytes(4)) 
        elif a[i] == "AAT": b.append(a[i]+" ") 
        elif a[i] == "VVT": b.append(a[i]+" ")
        elif a[i] == "AOO": b.append(a[i]+" ")
        elif a[i] == "AAI": b.append(a[i]+" ")
        elif a[i] == "VOO": b.append(a[i]+" ")
        elif a[i] == "VVI": b.append(a[i]+" ")
        elif a[i] == "VDD": b.append(a[i]+" ")
        elif a[i] == "DOO": b.append(a[i]+" ")
        elif a[i] == "DDI": b.append(a[i]+" ")
        elif a[i] == "DDD": b.append(a[i]+" ")
        elif a[i] == "AOOR": b.append(a[i])
        elif a[i] == "AAIR": b.append(a[i])
        elif a[i] == "VOOR": b.append(a[i])
        elif a[i] == "VVIR": b.append(a[i])
        elif a[i] == "VDDR": b.append(a[i])
        elif a[i] == "DOOR": b.append(a[i])
        elif a[i] == "DDIR": b.append(a[i])
        elif a[i] == "DDDR": b.append(a[i])
        else:
            try:
                b.append(int(i))
            except ValueError:
                b.append(i)
                  
    byte_b.append(b[0].encode())
    
    for i in range(1,26):
        if b[i]>=0:
            byte_b.append(b[i].to_bytes(byte_length[i], byteorder='big',signed=True))
        elif b[i]<0:
            byte_b.append(b[i].to_bytes(byte_length[i], byteorder='big',signed=True))



    print(byte_b)
    print(len(byte_b))
    #print(b)
    #print(len(a))




    #ser = serial.Serial('COM6', baudrate=115200)
    #print(ser.name)
    #cmd = b'\x16\x45\x55\x00'
    sum1 = 0 

    #WRITE_TEST
##    '''
##    cmd = b'\x16\x45\x55\x00'
##    a = 10
##    print(ser.write(cmd))
##    print(ser.write(bytes(50)))
##    #print(ser.read())
##    print(cmd)
##    #print(ser.read(10))
##    ser.close()
##    '''
    #READ_ECHO
##    cmd = b'\x16\x45\x49'
##    print(ser.write(cmd))
##    print(ser.write(bytes(51)))
##    a = ser.read(50)
##    print(a)
##    #print(cmd)
##    #print(ser.read(10))
##    ser.close()
##'''
##    #READ_EGRRAM
##    cmd = b'\x16\x45\x47'
##    print(ser.write(cmd))
##    print(ser.write(bytes(51)))
##    print(ser.read(50))
##    #print(cmd)
##    #print(ser.read(10))
##    ser.close()
##'''    
    #WRITE_VALUES
'''    
    cmd = b'\x16\x45\x55\x04'
    sum1 = sum1+ ser.write(cmd)
    for i in range(1,len(byte_b)):
        print(repr(byte_b[i]))
        sum1 =sum1 + ser.write(byte_b[i])
    print("total send:" , sum1)

    cmd1 = b'\x16\x45\x49'
    print(ser.write(cmd1))
    print(ser.write(bytes(51)))
    

    a = ser.read(50)
    print(a)
    #print(cmd)
    #print(ser.read(10))
    ser.close()
'''    
    

Load_Values("oscar")
##ser.write(bytes(1))
##ser.close()
