from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import struct,sys

expected=[0]*6
expected[0]=-5581       #ymin
expected[1]= 5268		#ymax
expected[2]=0x00061280	#oldXmin
expected[3]=0x0AD54780	#oldXmax
expected[4]=0x00070780	#newXmin
expected[5]=0x04C8DD80	#newXmax

dotsize=0.25
linesize=0.1
CRC=0x649D6B06

f=open("old-v2.dat","rb")
buf=f.read()
f.close()

lfcs_len=len(buf)//8
lfcs=[]
ftune=[]
err_correct=0

for i in range(lfcs_len):
	lfcs.append(struct.unpack("<I",buf[i*8:i*8+4])[0])

for i in range(lfcs_len):
	ftune.append(struct.unpack("<i",buf[i*8+4:i*8+8])[0])

f=open("new-v2.dat","rb")
buf=f.read()
f.close()

lfcs_new_len=len(buf)//8
lfcs_new=[]
ftune_new=[]

old=lfcs_len-1
new=lfcs_new_len-1
tot=old+new
title="old3DS[Blue]:%s + new3DS[Red]:%s = %s (v2)" %(str(old),str(new),str(tot))

for i in range(lfcs_new_len):
	lfcs_new.append(struct.unpack("<I",buf[i*8:i*8+4])[0])

for i in range(lfcs_new_len):
	ftune_new.append(struct.unpack("<i",buf[i*8+4:i*8+8])[0])
	
def to_hex(x, pos):
    return '%X' % int(x)

def report_data(input, expected, name, index):
	if(input != expected):
		if(index<2):
			print("%s has changed! %d -> %d !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" % (name,expected,input))
		else:
			print("%s has changed! %08X -> %08X !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" % (name,expected,input))

fmt = ticker.FuncFormatter(to_hex)
#greets to rubbleF15 for py3 hex ticker fix https://stackoverflow.com/questions/21189806/hexadecimal-x-axis-in-matplotlib
outstr=b"ymin:%d ymax:%d\nold3ds xmin:0x%X xmax:0x%X\nnew3ds xmin:0x%X xmax:0x%X\n" % (min(ftune_new),max(ftune),lfcs[1],max(lfcs),lfcs_new[1],max(lfcs_new))
names=["ymin","ymax","old3ds xmin","old3ds xmax","new3ds xmin", "new3ds xmax"]
input=[min(ftune_new),max(ftune),lfcs[1],max(lfcs),lfcs_new[1],max(lfcs_new)]

density_old=lfcs_len / ((max(lfcs)-lfcs[1])/256)
density_new=lfcs_new_len / ((max(lfcs_new)-lfcs_new[1])/256)
print("density: old-%.2f%% new-%.2f%%" % (density_old*100, density_new*100))

print(outstr)
for i in range(6):
	report_data(input[i], expected[i], names[i], i)

def graph(w,h):
	plt.figure(figsize=(w,h))
	plt.suptitle(title)
	axes = plt.gca()
	#axes.get_xaxis().set_major_locator(ticker.MultipleLocator(1))
	axes.get_xaxis().set_major_formatter(fmt)
	plt.plot(lfcs,ftune,'--bo',markersize=dotsize,linewidth=linesize)
	plt.plot(lfcs_new,ftune_new,'--ro',markersize=dotsize,linewidth=linesize)
	plt.axhline(0, color='gray')
	plt.axvline(0, color='gray')
	plt.xlabel('LFCS')
	plt.ylabel('msed3 error')
	plt.text(0x4E00000,50,"msed3=LFCS/5",fontsize=8)
	

graph(14,5)
plt.show()
graph(40,10) #bug workaround - savefig will remove the toolbar from view if used before show()
plt.savefig("%s/msed_data_v2_%08d.png" % (sys.path[0],tot))