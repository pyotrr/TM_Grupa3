def convolve_rir(audio_signal,rir):
    import numpy as np

    product = np.convolve(audio_signal, rir)

    return product
