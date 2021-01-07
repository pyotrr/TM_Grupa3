

def get_rir(audio_signal, fs, rt60=0.3, room_dim =[20, 20, 12], room_source=[6, 15, 9], mic_pos=[10, 10, 6], T=6, D=7, S=35):
    import pyroomacoustics as pra
    import numpy as np
    c=1449.2+4.6*T-0.055*T**2+0.0029*T**3+(1.34-0.01*T)*(S-35)+0.016*D
    e_absorption, max_order = pra.inverse_sabine(rt60, room_dim, c=c)
    room = pra.ShoeBox(
        room_dim, fs=fs, materials=pra.Material(e_absorption), max_order=5
    )
    room.add_source(room_source, signal=audio_signal, delay=1.0)
    mic_locs = np.c_[
        mic_pos,  # mic 1
    ]
    room.add_microphone_array(mic_locs)
    room.compute_rir()
    rir = room.rir[0][0]
    return rir

def convolve_rir(audio_signal,rir):
    import numpy as np
    rir=rir[1000:8000]
    product = np.convolve(audio_signal, rir)

    return product
