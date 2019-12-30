# nodes
* old-v2.dat and new-v2.dat are database files used by [seedminer](https://github.com/zoogie/seedminer) to improve movable.sed keyY brute force speed. They have been moved from that repo to clean up its commit history.  
* graph.py will take both .dat files and produce a chart that plots msed data. This graph shows the mathematical relationship between a 3DS's LocalFriendCodeSeed (LFCS, X-axis), and the last u32 of its movable.sed keyY (distance from LFCS/5, Y-axis). This relationship is what makes the bruteforce possible. More details: [34⅕c3](https://zoogie.github.io/web/34%E2%85%95c3/#/)
* You need matplotlib installed and I think it only runs in python 2 correctly.
