
from scipy.signal import kaiser_beta, lfilter, firwin, freqz

def lpf(sample_rate,x,cutoff_hz=500.0, attenuation = 25):

  nyq_rate = sample_rate / 2.0
  attenuation=attenuation
  N=100
  beta = kaiser_beta(attenuation)
  cutoff_hz = cutoff_hz
  taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
  filtered_x = lfilter(taps, [1.0,0], x)
  return filtered_x

