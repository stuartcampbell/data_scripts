import os
from datetime import date, timedelta
import pandas as pd
import argparse


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        print(f"checking {dirpath}")
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

#print get_size()



def get_filesize_table(root_dir, start="2015-01-01", stop="2018-12-31"):
    # start and end this date
    start_tp = [int(i) for i in start.split("-", maxsplit=2)]
    stop_tp = [int(i) for i in stop.split("-", maxsplit=2)]
    if len(start_tp) != 3:
        raise ValueError(f"Error, did not get yyyy-mm-dd. Got: {start_tp}")

    if len(stop_tp) != 3:
        raise ValueError(f"Error, did not get yyyy-mm-dd. Got: {stop_tp}")

    d1 = date(*start_tp)  # start date
    d2 = date(*stop_tp)  # end date
    #ROOT = "/home/lhermitte/tmp"

    delta = d2 - d1         # timedelta

    df = pd.DataFrame()

    for i in range(delta.days + 1):
        new_date = d1 + timedelta(i)
        subdir = f'{new_date.year:04}/{new_date.month:02}/{new_date.day:02}'
        sz = get_size(root_dir + "/" + subdir)
        df = df.append(pd.Series(dict(date=new_date, size=sz)),
                       ignore_index=True)#, name=new_date))
    return df

if __name__ == "__main__":
    '''
        Walks through directories in a yyyy/mm/dd structure and obtains file
        sizes. Saves file size total per day.
    '''

    parser = argparse.ArgumentParser(description='Scrape the date directory tree for file sizes.')
    parser.add_argument('-r', '--root', dest='root_dir', type=str,
                    help='The root directory', default='.')
    parser.add_argument('-o', '--output_file', dest='output_file', type=str,
                    help='The root directory', default='dat.txt')
    parser.add_argument('-t1', '--start', dest='start', type=str,
                    help='Start time', default='2015-01-01')
    parser.add_argument('-t2', '--stop', dest='stop', type=str,
                    help='Start time', default='2018-12-31')

    args = parser.parse_args()
    df = get_filesize_table(args.root_dir, start=args.start, stop=args.stop)
    df.to_csv(args.output_file, sep=" ", index=False)
