"""
The main script designed to execute the Purdue CAM2 Team's One Billion Image Experiment

*****************************
Usage: python exp_runner.py

******************************
    ** THE CAM2 PROJECT **
******************************
Authors: Caleb Tung,
Created: 10/12/2017
Preferred: Python3.x
"""
from __future__ import print_function # Force the use of Python3.x print()

import getopt
import sys
import speedtest

def report_down_up(is_print_details=False):
    """
    Reports the download/upload speeds of the current machine to the nearest speedtest.net server

    param: is_print_details (default FALSE) - turns on printing of speedtest results to stdout

    return: An array [download, upload] speed in bits/sec
    """
    stest = speedtest.Speedtest()
    stest.get_best_server()
    stest.download()
    stest.upload()

    test_results = stest.results.dict()
    if is_print_details:
        print(test_results)

    return [test_results.get("download"), test_results.get("upload")]

def csv_down_up(down_up_arr, data_file):
    """
    Writes the upload/download data to a CSV file

    param: down_up_arr - An array [download, upload] speed in bits/sec
    param: data_file - A file pointer to an open CSV file

    return: None
    """
    down_speed = str(down_up_arr[0])
    up_speed = str(down_up_arr[1])

    data_file.write(down_speed + "," + up_speed + "\n")

def _show_help():
    print("USAGE: python " + sys.argv[0] + " -i <num of iterations to run speedtest>" \
          + " -f <output CSV filepath> -p <True/False to print details to stdout; default = False>")

def _main():
    try:
        opts, unused_args = getopt.getopt(sys.argv[1:], "i:f:p",
                                          ["iterations=", "filepath=", "printdetails="])
    except getopt.GetoptError:
        _show_help()
        sys.exit(2)

    num_iters = 1
    file_path = None
    is_print_details = False

    for [opt, arg] in opts:
        if opt in ("-h", "--help"):
            _show_help()
            sys.exit(2)
        elif opt in ("-i", "--iterations"):
            num_iters = int(arg)
        elif opt in ("-f", "--filepath"):
            file_path = arg
        elif opt in ("-p", "--printdetails"):
            is_print_details = bool(arg)

    csv_file = open(file_path, "a")

    for i in range(0, num_iters):
        print("Test " + str(i))
        stest_results = report_down_up(is_print_details)
        csv_down_up(stest_results, csv_file)

    csv_file.close()

    return 0

if __name__ == '__main__':
    _main()
