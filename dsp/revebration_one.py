
def get_rir(fs, rt60=0.2,
            room_dim=[60, 60, 10],
            room_source=[30, 30, 4.5],
            mic_pos=[30, 10, 7],
            T=19, D=0.01, S=35,
            save_to_wav=False):
    import pyroomacoustics as pra
    import numpy as np
    c = 1449.2+4.6*T-0.055*T**2+0.0029*T**3+(1.34-0.01*T)*(S-35)+0.016*D
    e_absorption, max_order = pra.inverse_sabine(rt60, room_dim, c=c)
    room = pra.ShoeBox(
        room_dim, fs=fs, materials=pra.Material(e_absorption),ray_tracing=False, max_order=3 ,air_absorption=False
    )
    room.add_source(room_source, delay=1.0)
    mic_locs = np.c_[
        mic_pos,  # mic 1
    ]
    room.add_microphone_array(mic_locs)
    room.compute_rir()
    rir = room.rir[0][0]
    return rir


def convolve_rir(audio_signal,rir):
    import numpy as np

    product = np.convolve(audio_signal, rir)

    return product
