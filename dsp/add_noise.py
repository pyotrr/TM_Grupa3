from scipy import signal


def add_noise(data, noise, fs_data, fs_noise=48000):
    import numpy as np
    if fs_noise != fs_data:
        noise = signal.resample(noise, len(data))
    if len(noise) > len(data):
        noise = noise[range(0, len(data))]
    else:
        diff = len(data) - len(noise)
        n_noise = diff/len(noise)
        long_noise = np.array(noise, copy=True)
        while n_noise >= 0:
            long_noise = np.concatenate((long_noise, noise))
            n_noise -= 1
        noise = long_noise
        noise = noise[range(0, len(data))]
        noise=noise/abs(max((noise)))
        data=data/abs(max(data))
    result = 0.9 * data + 0.1 * noise
    return result
