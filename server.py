import socket,csv,datetime
s = socket.socket()

host = '192.168.43.39'
port = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(2)
print('waiting for first client')
conn1, addr1 = server.accept()
print('Connected by client: %s' % repr(addr1))
print('waiting for second client')
conn2, addr2 = server.accept()
print('Connected by client: %s' % repr(addr1))

def connrun():
    data = conn1.recv(1024)
    return data
def conn1run():
    data = conn2.recv(1024)
    return data

currenttime = datetime.datetime.now()
currenttime = str(currenttime)
currenttime_array = currenttime.split(' ')
date = currenttime_array[0]
time = currenttime_array[1][:8]
mode = time.split(':')
s1 = int(mode[0])
s2 = int(mode[1])
s3 = int(mode[2])
s1 = s1*10000+s2*100+s3
time = s1
mode = date.split('-')
s1 = int(mode[0])
s2 = int(mode[1])
s3 = int(mode[2])
s1 = s1*10000+s2*100+s3
date = s1
filename = 'output'+str(time)+'_'+str(date)
filename+='.csv'
print('Name of File created :',filename)
header_name = ["Date","Time","lat1","lng1","alt1","pitchd1","yawd1","yawo1","pitcho1","lat2","lng2","alt2","pitchd2","yawd2","yawo2","pitcho2"]

with open(filename, 'w+') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header_name)
while True:
    data1=connrun()
    data2 = conn1run()
    data1 = data1.decode()
    data2 = data2.decode()
    data1 = data1.split('\n')
    data1 = data1[-2]
    data2 = data2.split('\n')
    data2 = data2[-2]
    data1 = data1.split(',')
    data2 = data2.split(',')
    currenttime = datetime.datetime.now()
    currenttime = str(currenttime)
    currenttime_array = currenttime.split(' ')
    date = currenttime_array[0]
    Time = currenttime_array[1][:8]
    if(len(data1)!=8):
        continue
    if(len(data2)!=8):
        continue
    if(data1[-1].split(':')[1]=='1'):
        lat1 = data1[0].split(':')[1]
        lng1 = data1[1].split(':')[1]
        alt1 = data1[2].split(':')[1]
        pitchd1 = data1[3].split(':')[1]
        yawd1 = data1[4].split(':')[1]
        yawo1 = data1[5].split(':')[1]
        pitcho1 = data1[6].split(':')[1]
        print(lat1,lng1,alt1,pitchd1,yawd1,yawo1,pitcho1)
        lat2 = data2[0].split(':')[1]
        lng2 = data2[1].split(':')[1]
        alt2 = data2[2].split(':')[1]
        pitchd2 = data2[3].split(':')[1]
        yawd2 = data2[4].split(':')[1]
        yawo2 = data2[5].split(':')[1]
        pitcho2 = data2[6].split(':')[1]
        print(lat2,lng2,alt2,pitchd2,yawd2,yawo2,pitcho2)
        data_list = [date,Time,lat1,lng1,alt1,pitchd1,yawd1,yawo1,pitcho1,lat2,lng2,alt2,pitchd2,yawd2,yawo2,pitcho2]
        with open(filename, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data_list)
    else:
        lat2 = data1[0].split(':')[1]
        lng2 = data1[1].split(':')[1]
        alt2 = data1[2].split(':')[1]
        pitchd2 = data1[3].split(':')[1]
        yawd2 = data1[4].split(':')[1]
        yawo2 = data1[5].split(':')[1]
        pitcho2 = data1[6].split(':')[1]
        
        lat1 = data2[0].split(':')[1]
        lng1 = data2[1].split(':')[1]
        alt1 = data2[2].split(':')[1]
        pitchd1 = data2[3].split(':')[1]
        yawd1 = data2[4].split(':')[1]
        yawo1 = data2[5].split(':')[1]
        pitcho1 = data2[6].split(':')[1]
        print(lat1,lng1,alt1,pitchd1,yawd1,yawo1,pitcho1)
        print(lat2,lng2,alt2,pitchd2,yawd2,yawo2,pitcho2)
        data_list = [date,Time,lat1,lng1,alt1,pitchd1,yawd1,yawo1,pitcho1,lat2,lng2,alt2,pitchd2,yawd2,yawo2,pitcho2]
        with open(filename, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data_list)
        
