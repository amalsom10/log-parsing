# log-parsing
## RUN THE SCRIPT AS BELOW
### If you want to completly parse the file and the access log in available in the same location
```
--> python3 main.py

OUTPUT:
2XX occurrence in time frame: 71591 
4XX occurrence in time frame: 2030 
5XX occurrence in time frame: 6778 
Bytes sent in time frame: 1150283652 
50th percentile: 6778.0 
90th percentile: 58628.4 
95th percentile: 65109.7 
100th percentile: 71591.0 

```
### If you have different timeframe to check and you want to pass a path for file 
```
---> python3 main.py --help 
usage: Script to parse the nginx logs [-h] [--starttime ST_TIME]
                                      [--endtime END_TIME] [--file FILE_PATH]

optional arguments:
  -h, --help           show this help message and exit
  --starttime ST_TIME
  --endtime END_TIME
  --file FILE_PATH

```
```
---> python3 main.py --starttime 27/May/2020:12:37:10 --endtime 27/May/2020:12:39:24 --file access.log 

output
2XX occurrence in time frame: 362 
4XX occurrence in time frame: 4 
5XX occurrence in time frame: 32 
Bytes sent in time frame: 7069307 
50th percentile: 32.0 
90th percentile: 296.0 
95th percentile: 328.99999999999994 
100th percentile: 362.0 
``` 

##Requiremnts
```
--->  pip3 freeze

numpy==1.18.4
```
