"""
Assignment: FFT (Recursive and Iterative)
Authored by: O Guneshwor Singh
 
DATE: 26-Mar-2014
-----------------------------------------------
Requirements:
    Python 3+
    
-----------------------------------------------
Usage:

>>> python fft.py <file.csv>

<file.csv> must be passed as an argument

Output:

* Two csv files - recursive and iterative
* Times spent by each of them

Limitation:
The number of data points from the file are ass-
med to be even

"""
import csv
import math
import sys
from cmath import exp, pi
import timeit

data = []

f = open(sys.argv[1], 'r') # opens the csv file
try:
    reader = csv.reader(f, delimiter = ',')  # creates the reader object
    for row in reader:   # iterates the rows of the file in orders
    	data = [float(x) for x in row]
finally:
    f.close()      

# Recursive FFT
def recursive_fft(x):
    n = len(x)
    if n <= 1: return x

    even = recursive_fft(x[0::2])
    odd =  recursive_fft(x[1::2])
    y0 = [even[k] + exp(-2j * pi * k / n)*odd[k] for k in range(int(n/2))] 
    y1 = [even[k] - exp(-2j * pi * k / n)*odd[k] for k in range(int(n/2))]
    y = y0 +y1
    return y


res = recursive_fft (data)
print("Recursive FFT:")
print (res)

resultFile = open("outputRecusive.csv",'w')
wr = csv.writer(resultFile, dialect='excel')
wr.writerow(res)


#
# Iterative fft 
def nextpower2(i):
    n = 2
    while n < i: n = n * 2
    return n

def bitrev(x):
    #return x[::-1]
    N = len(x)
    if N != nextpower2(N): 
        print("error")
        exit(0)

    x = x[:]
    for i in range(N):
        k, b, a = 0, N>>1, 1
        while b >= a:
            if b&i: k = k|a
            if a&i: k = k|b
            b, a = b>>1, a<<1
        if i < k:               
            x[i], x[k] = x[k], x[i]
    return x
#@timeit
def iterative_fft(x):
    n = len(x)
    X = []
    x = bitrev(x)
    for i in range(n):      
        X.append(exp(-2j * pi * i /n))
    m = 2
    while m <= n:
        for s in range(0,n, m):
            for i in range(int(m/2)):
                p = i *int(n/ m)
                a = s + i
                b = s + i + int(m/2)
                x[a], x[b] = x[a] + X[p%n] * x[b], x[a] - X[p%n] * x[b]
        m = m * 2
    return x

# print()
# print (iterative_fft([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]))

# print()
# print(recursive_fft([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]))
print()
#print(recursive_fft([0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]))
res = iterative_fft(data)
print("Iterative FFT:")
print(res)

resultFile = open("outputIterative.csv",'w')
wr = csv.writer(resultFile, dialect='excel')
wr.writerow(res)

# Measuring times spent

print("\nTime spent:")
t=timeit.Timer("recursive_fft(data)","from __main__ import recursive_fft, data")
print ("Recursive: %0.4f us" %(t.timeit(1)* 1000000))

t=timeit.Timer("iterative_fft(data)","from __main__ import iterative_fft, data")
print ("Iterative: %0.4f us" %(t.timeit(1)* 1000000))
