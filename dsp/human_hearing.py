from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz

def lpf(sample_rate,x,cutoff_hz=500.0, width = 250.0,ripple_db = 25.0):

  nyq_rate = sample_rate / 2.0
  width = width/nyq_rate
  ripple_db = ripple_db
  N, beta = kaiserord(ripple_db, width)
  cutoff_hz = cutoff_hz
  taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
  filtered_x = lfilter(taps, 1.0, x)

  return filtered_x
