import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import struct,sys,binascii

dotsize=0.5
linesize=0.1

f=open("lfcs.dat","rb")
buf=f.read()
f.close()

lfcs_len=len(buf)//8
lfcs=[]
ftune=[]
err_correct=0

for i in range(lfcs_len):
	lfcs.append(struct.unpack("<I",buf[i*8:i*8+4])[0]<<12 or 0x800)

for i in range(lfcs_len):
	ftune.append(struct.unpack("<i",buf[i*8+4:i*8+8])[0])

f=open("lfcs_new.dat","rb")
buf=f.read()
f.close()

lfcs_new_len=len(buf)//8
lfcs_new=[]
ftune_new=[]

old=lfcs_len-1
new=lfcs_new_len-1
tot=old+new
title="old3DS[Blue]:%s + new3DS[Red]:%s = %s" %(str(old),str(new),str(tot))

for i in range(lfcs_new_len):
	lfcs_new.append(struct.unpack("<I",buf[i*8:i*8+4])[0]<<12 or 0x800)

for i in range(lfcs_new_len):
	ftune_new.append(struct.unpack("<i",buf[i*8+4:i*8+8])[0])
	
def to_hex(x, pos):
    return '%X' % int(x)
fmt = ticker.FuncFormatter(to_hex)
#greets to rubbleF15 for py3 hex ticker fix https://stackoverflow.com/questions/21189806/hexadecimal-x-axis-in-matplotlib
outstr=b"ymin:%d ymax:%d\nold3ds xmin:0x%X xmax:0x%X\nnew3ds xmin:0x%X xmax:0x%X" % (min(ftune_new),max(ftune),lfcs[1],max(lfcs),lfcs_new[1],max(lfcs_new))
print(outstr)
crc=binascii.crc32(outstr)
print("data crc32 %08X" % crc)
if(crc != 0x7E8598B0):
	print("DATA HAS CHANGED!!\n"*20)
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
graph(160,40) #bug workaround - savefig will remove the toolbar from view if used before show()
plt.savefig("msed_data_%08d.png" % tot)