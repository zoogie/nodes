rm old-v2.dat
rm new-v2.dat
bitsadmin.exe /transfer "old" https://github.com/zoogie/nodes/blob/master/old-v2.dat?raw=true %cd%/old-v2.dat
bitsadmin.exe /transfer "new" https://github.com/zoogie/nodes/blob/master/new-v2.dat?raw=true %cd%/new-v2.dat
pause
