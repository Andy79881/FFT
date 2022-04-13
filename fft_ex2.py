# FFT of csv time domain data from MDO3054 scope
# Author: A. Nestler
# source based from:
# https://www.cbcity.de/die-fft-mit-python-einfach-erklaert
# generated signal with FFT from NumPy
# 1) read raw data (time, value) in time domain from csv (func read_csv)
# 2) set initial time (func read_csv)
# 3) perform FFT with window, plot time and frequency domain data (func _fft)

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description="FFT from scope csv raw data file")
# from scipy.fftpack import fft, ifft

# plt.style.use('seaborn-poster')

# parse for arguments on commandline
# returns arguments
# access via key words in dest
def parse_args():
    parser.add_argument("-f", "--file",
                        dest="filename",
                        default="tek0001CH4.csv",
                       # type=argparse.FileType('r', encoding='UTF-8'),
                       # required=True,
                        help="csv input file name")
    parser.add_argument("-w", "--window", dest="window", default="hamm")
    args = parser.parse_args()
    return args

# read data from csv, return values: time, value
# arguments: file name, visualize [Boolean]
# set header accordingly to header row -1
def read_csv(fname, visualize):
    df = pd.read_csv(fname,
                          sep=",",
                          header=19, 
                          names = ["time", "val"])
    print(df.head()) 
    df.time = df.time - df.time[0] # start at time = 0s
    print('set initial time to 0s...')
    print(df.head())
    ts = df.time[1]
    print('Sampling time ts: ', ts)
    if visualize == True:
        plt.figure(figsize = (8, 6))
        plt.plot(df.time,df.val)
        plt.xlabel('time (s)')
        plt.ylabel('Current (A)')

        plt.show()
    return df.time, df.val

# creates a test signal to verify correct FFT algorithmn
# return values: time, value
# set parameters f, A and time step accordingly
def sine_test_signal(visualize):
    t = np.linspace(0, 0.004, 1001, endpoint=True)
    f = 20000.0 # Frequency in Hz
    A = 1.0 # Amplitude in Unit
    s = A * np.sin(2*np.pi*f*t) # Signal
    # data.time=t
    # data.val=s
    # print(s)
    if visualize == True:
        plt.plot(t,s)
        plt.xlabel('Time ($s$)')
        plt.ylabel('Amplitude ($Unit$)')
        plt.show()

    data = s
    return t, data
    

# function _fft to perform FFT from data with window
def _fft(t, data, title_appendix): 
    # x = data.time
    # y = data.val
    x = t
    y = data
    tappendix = title_appendix
 
    # for real physical values of frequency
    Ts = x[1]-x[0] # sampling time
    fs = 1.0/Ts # sampling frequency
    print('dt=%.5fs (Sample Time)' % Ts)
    print('fa=%.2fHz (Frequency)' % fs)
    N = int(len(y)/2+1)
    X = np.linspace(0, fs/2, N, endpoint=True)
    print("Frequency interval: ", X[:4])

    # windowing
    # dictionary with window functions to pick one of them
    # argument y required to pass the data for length calculation
    win_func = {
        "hann" : lambda y : np.hanning(len(y)),
        "hamm" : lambda y : np.hamming(len(y)),
        "black" : lambda y : np.blackman(len(y))     
    }
    # second dictionary with full text name of window function
    # used for print
    win_func_fulltext = {
      "hann" : "Hanning",
      "hamm" : "Hamming",
      "black": "Blackman" 
    }
    win = args.window # get win from CLI arguments
    if win in win_func:
        print("Window function: ", win_func_fulltext[win])
        Ywindow = np.fft.fft(win_func[win](y)*y)
    else: 
        print("Valid window functions: ", win_func_fulltext)
        parser.error("{} is no valid window function!".format(win))
    
    print('N: ', N)
    Ywindow[0] = 0 # remove DC 
    Ywindow[1] = 0 # remove DC 
    # print(np.abs(Y))
    
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1) # first subplot upper horizontal
    ax2 = fig.add_subplot(2, 1, 2) # second subplot lower horizontal
    
    plt.subplot(211)
    ax1.plot(x*1000, y, 'r') # scale for ms
    ax1.set_xlabel('time ($ms$)')
    ax1.set_ylabel('Current ($A$)')
    ax1.grid(color='k', linestyle='dashed')
    title_base = 'time domain raw data - '
    plt_title1 = title_base+tappendix
    ax1.set_title(plt_title1)
   
    plt.subplot(212) 
    ax2.plot(X, 2*1000*np.abs(Ywindow[:N])/N, 'b') # scale for mA
    ax2.set_xscale("log")
    # ax2.set_xlim([N/10, N])
    # ax2.set_ylim(0, 0.1) # scale accordingly the max value
    ax2.set_xlabel('frequency ($Hz$)')
    ax2.set_ylabel('Current ($mA$)')
    ax2.grid(color='k', linestyle='dashed')
    title_base = 'FFT with Window function: '
    plt_title2 = title_base+win_func_fulltext[win]
    ax2.set_title(plt_title2)
    
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    args = parse_args()
    fname = args.filename  # extract file name
    # t, data=read_csv("tek0001CH4.csv",False)
    t, data=sine_test_signal(False) # sine test data
    _fft(t, data, "sine test signal") # FFT from test data
    t, data=read_csv(fname,False)
    # t, data=input_signal()
    _fft(t, data, fname)
    
    

