import argparse
import datetime
import logging
import sys
import numpy as ny

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')
logger = logging.getLogger()


def log_fetch(st_time, end_time, file):
    stat_dict = dict();
    stat_dict['2XX'] = 0
    stat_dict['4XX'] = 0
    stat_dict['5XX'] = 0
    stat_dict['UNKNOWN'] = 0
    stat_dict['Bytesused'] = 0
    try:
        with open(file, "r") as logs:
            for line in logs:
                date = datetime.datetime.strptime(line.split(" ")[0].split("[")[1], '%d/%b/%Y:%H:%M:%S')
                if st_time <= date <= end_time:
                    try:
                        res = int(line.split(" ")[5])
                    except(ValueError, TypeError):
                        continue
                    if res in range(200, 204):
                        stat_dict['2XX'] += 1
                    elif res in range(400, 404):
                        stat_dict['4XX'] += 1
                    elif res in range(500, 504):
                        stat_dict['5XX'] += 1
                    else:
                        stat_dict['UNKNOWN'] +=1
                    byte_read = int(line.split(" ")[6])
                    stat_dict['Bytesused'] += byte_read
        return stat_dict
    except (FileNotFoundError, IOError):
        logger.info("Error in reading the file, please try again")
        return 0


def percent(arr, per):
    try:
        pe = ny.percentile(arr, per)
        return pe
    except :
        logger.info("Error in calculating percentile")
        return 0


def time_check(time):
    try:
        r_time = datetime.datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
        return r_time
    except (ValueError, TypeError):
        logger.info("Please enter the start time and end time in format D/M/Y:H:M:S , Please try again")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Script to parse the nginx logs")
    parser.add_argument("--starttime", action="store", dest="st_time", type=str, required=False, default="01/Jan/0001:00:00:00")
    parser.add_argument("--endtime", action="store", dest="end_time", type=str, required=False, default="31/Dec/9999:00:00:00")
    parser.add_argument("--file", action="store", dest="file_path", type=str, required=False, default="access.log")
    args = parser.parse_args()
    file_path = args.file_path
    start_time = time_check(args.st_time)
    en_time = time_check(args.end_time)
    if en_time <= start_time or en_time == 0 or start_time == 0:
        logger.info("end time should be larger than start time or issue with the time format")
        exit(0)
    stats = log_fetch(start_time, en_time, file_path)
    if stats == 0:
        exit(0)
    else:
        logger.info("2XX occurrence in time frame: {} \n4XX occurrence in time frame: {} \n"
                    "5XX occurrence in time frame: {} \nBytes sent in time frame: {} ".format(stats['2XX'], stats['4XX'], stats['5XX'], stats['Bytesused']))
    stats_arr = []
    stats_arr.append(stats['2XX'])
    stats_arr.append(stats['4XX'])
    stats_arr.append(stats['5XX'])
    logger.info("50th percentile: {} ".format(percent(stats_arr, 50)))
    logger.info("90th percentile: {} ".format(percent(stats_arr, 90)))
    logger.info("95th percentile: {} ".format(percent(stats_arr, 95)))
    logger.info("100th percentile: {} ".format(percent(stats_arr, 100)))
