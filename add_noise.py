from scipy import signal
def add_noise(data,noise,fs_data,fs_noise):
    if fs_noise != fs_data:
        noise = signal.resample(noise, len(data))
    if len(noise) > len(data):
        noise = noise[range(0,len(data))]
    else:
        data = data[range(0,len(noise))]
    result = 0.5 * data + 0.5 * noise
    return  result