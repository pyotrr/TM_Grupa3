from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz

def lpf(sample_rate,x,cutoff_hz=1000.0, width = 5.0,ripple_db = 18.0):

  nyq_rate = sample_rate / 2.0
  width = width/nyq_rate
  ripple_db = ripple_db
  N, beta = kaiserord(ripple_db, width)
  cutoff_hz = cutoff_hz
  taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
  filtered_x = lfilter(taps, 1.0, x)


  return filtered_x

def hpf(sample_rate,x,cutoff_hz=500.0, width = 1.0,ripple_db =8.0):

  nyq_rate = sample_rate / 2.0
  width = width/nyq_rate
  ripple_db = ripple_db
  N, beta = kaiserord(ripple_db, width)
  if N % 2 == 0:
    N = N + 1
  cutoff_hz = cutoff_hz
  taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta),pass_zero=False)
  filtered_x = lfilter(taps, 1.0, x)

  return filtered_x