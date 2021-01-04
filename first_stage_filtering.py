def calculate_alfa(T, D, S, pH):
    #Charakterystyka filtra dla odleglosci 1km dźwięku # zmiana3
    import math
    import numpy as np
    table = []
    f1 = 0.78*math.sqrt(S/35)*math.exp(T/26)
    f2 = 42*math.exp(T/17)
    for f in range(1, 20001):
        if f > 100:
            f = f/1000 # podane w kHz
            alfa = 0.106*((f1*f**2)/(f1**2+f**2))*math.exp((pH-8)/0.56)+0.52*(1+T/43)*(S/35)*((f2*f**2)/(f2**2+f**2))*math.exp(-D/6)+0.00049*f**2*math.exp(-(T/27+D/17))
            table.append(alfa)
        else:
            alfa = 0
            table.append(alfa)
    ideal_response = np.array(table)
    return ideal_response

def prepare_filtering_one(ideal_response, N):
    import scipy.signal
    import numpy as np

    ideal_response = ideal_response
    ideal_response = 10 ** (-ideal_response / 20)
    ideal_response = ideal_response - ideal_response[-1]
    ideal_response = ideal_response * (1 / ideal_response[0])
    #Powyżej krótka normalizacja odpowiedzi filtra do funkcji firwin2

    freq=np.linspace(0, 1, len(ideal_response))


    fir = scipy.signal.firwin2(N, freq, ideal_response)

    return fir

def do_filtering(file, fir):
    import numpy as np
    import scipy.signal

    a = [1.0, 0]
    b = fir

    w, h = scipy.signal.freqz(b, a)

    product = np.convolve(file, h)
    return product

