import tkinter.filedialog
import tkinter as tk
import simpleaudio as sa
import first_stage_filtering as ff
import revebration_one as ro
import human_hearing as hh


class GUI:
    width = 800
    height = 600

    audio_file = []
    filtered_audio_file = []
    human_hearing = []

    rate = 0
    bytes_per_sample = 2

    def __init__(self, master):
        self.master = master

        master.title('Wasser')
        self.canvas = tk.Canvas(master, height=self.height, width=self.width, bg='#b8cbe6')
        self.canvas.pack()
        self.input_frame = tk.Frame(master)
        self.input_frame.place(relwidth=0.8, relheight=0.05, relx=0.1, rely=0.1)

        self.path_input = tk.Entry(self.input_frame)
        self.path_input.place(relwidth=0.9, relheight=1)
        self.path_input.insert(0, 'Select file...')
        self.path_input.bind('<Button-1>', self.select_file_from_modal)

        self.path_button = tk.Button(self.input_frame, text='Open')
        self.path_button.place(relwidth=0.1, relheight=1, relx=0.9)
        self.path_button.bind('<Button-1>', self.load_file)

        self.player_frame = tk.Frame(master)
        self.play_button_text = tk.StringVar()
        self.play_button_text.set('Play')
        self.play_button = tk.Button(self.player_frame, textvariable=self.play_button_text, name='play_unfiltered')
        self.play_button.bind('<Button-1>', self.play_loaded_audio)
        self.file_name = tk.StringVar()
        self.file_name_label = tk.Label(self.player_frame, textvariable=self.file_name)

        self.apply_filter_button = tk.Button(master, text='Apply filter!', name='filter')
        self.apply_filter_button.bind('<Button-1>', self.apply_first_filtration)

        self.filtered_player_frame = tk.Frame(master)
        self.filtered_play_button_text = tk.StringVar()
        self.filtered_play_button_text.set('Play')
        self.filtered_play_button = tk.Button(
            self.filtered_player_frame, textvariable=self.filtered_play_button_text, name='play_filtered'
        )
        self.filtered_save_button = tk.Button(
            self.filtered_player_frame, text='Save', name='save_filtered'
        )
        self.filtered_save_button.bind('<Button-1>', self.save_to_file)
        self.filtered_play_button.bind('<Button-1>', self.play_loaded_audio)
        self.filtered_file_name = tk.StringVar()
        self.filtered_file_name_label = tk.Label(
            self.filtered_player_frame, textvariable=self.filtered_file_name
        )

        self.simulate_hh_button = tk.Button(master, text='Simulate human hearing!', name='simulate')
        self.simulate_hh_button.bind('<Button-1>', self.simulate_human_hearing)

        self.hh_player_frame = tk.Frame(master)
        self.hh_play_button_text = tk.StringVar()
        self.hh_play_button_text.set('Play')
        self.hh_play_button = tk.Button(
            self.hh_player_frame, textvariable=self.hh_play_button_text, name='play_hh'
        )
        self.hh_save_button = tk.Button(
            self.hh_player_frame, text='Save', name='save_hh'
        )
        self.hh_save_button.bind('<Button-1>', self.save_to_file)
        self.hh_play_button.bind('<Button-1>', self.play_loaded_audio)
        self.hh_file_name = tk.StringVar()
        self.hh_file_name_label = tk.Label(
            self.hh_player_frame, textvariable=self.hh_file_name
        )

    def select_file_from_modal(self, event):
        self.path_input.config(state='normal')
        current_input_value = self.path_input.get()
        self.path_input.delete(0, len(current_input_value))
        path = tk.filedialog.askopenfilename(filetypes=[('WAV Files', '*.wav;*.WAV')])
        self.path_input.insert(0, path)
        return

    def load_file(self, event):
        path = self.path_input.get()
        if not path.endswith('.wav'):
            return

        import scipy.io.wavfile
        import numpy as np

        self.path_input.config(state='disabled')

        rate, data = scipy.io.wavfile.read(path)
        if len(np.shape(data)) == 2:
            data = data[:, 0]
        data = data / max(abs(data))

        self.audio_file = data
        self.rate = rate
        self.player_frame.place(relwidth=0.5, relheight=0.05, relx=0.25, rely=0.2)
        split_path = path.split('/')
        self.file_name.set(split_path[len(split_path) - 1])
        self.file_name_label.place(relwidth=0.8, relheight=1)
        self.play_button.place(relwidth=0.2, relheight=1, relx=0.8)
        self.apply_filter_button.place(relwidth=0.1, relheight=0.05, relx=0.45, rely=0.3)
        return

    def play_loaded_audio(self, event):
        import numpy as np

        player_button = str(event.widget).split('.')[-1]

        if player_button == 'play_unfiltered':
            selected_audio_file = self.audio_file
            button_label = self.play_button_text
        elif player_button == 'play_filtered':
            selected_audio_file = self.filtered_audio_file
            button_label = self.filtered_play_button_text
        else:
            selected_audio_file = self.human_hearing
            button_label = self.hh_play_button_text

        data = (selected_audio_file * 32767 / max(abs(selected_audio_file)))
        data = data.astype(np.int16)

        if event.widget['text'] == 'Play':
            button_label.set('Stop')
            sa.stop_all()
            play_obj = sa.play_buffer(data, 1, self.bytes_per_sample, self.rate)
        else:
            button_label.set('Play')
            sa.stop_all()
        return

    def apply_first_filtration(self, event):
        ideal_filter = ff.calculate_alfa()
        fir = ff.prepare_filtering_one(ideal_filter)
        product = ff.do_filtering(self.audio_file, fir)

        rir = ro.get_rir(product, self.rate)
        self.filtered_audio_file = (ro.convolve_rir(product, rir)) # usunalem abs

        self.filtered_player_frame.place(relwidth=0.5, relheight=0.05, relx=0.25, rely=0.4)
        self.filtered_file_name.set(self.file_name_label['text'] + ' (filtered)')
        self.filtered_file_name_label.place(relwidth=0.6, relheight=1)
        self.filtered_play_button.place(relwidth=0.2, relheight=1, relx=0.6)
        self.filtered_save_button.place(relwidth=0.2, relheight=1, relx=0.8)

        self.simulate_hh_button.place(relwidth=0.2, relheight=0.05, relx=0.40, rely=0.5)

    def simulate_human_hearing(self, event):
        self.human_hearing = hh.lpf(self.rate, self.filtered_audio_file)

        self.hh_player_frame.place(relwidth=0.5, relheight=0.05, relx=0.25, rely=0.6)
        self.hh_file_name.set(self.file_name_label['text'] + ' (human hearing)')
        self.hh_file_name_label.place(relwidth=0.6, relheight=1)
        self.hh_play_button.place(relwidth=0.2, relheight=1, relx=0.6)
        self.hh_save_button.place(relwidth=0.2, relheight=1, relx=0.8)

    def save_to_file(self, event):
        import scipy.io.wavfile

        save_button = str(event.widget).split('.')[-1]
        path = tk.filedialog.asksaveasfilename(filetypes=[('WAV Files', '*.wav;*.WAV')])

        if save_button == 'save_filtered':
            data = self.filtered_audio_file
        else:
            data = self.human_hearing
        if path.endswith('.wav'):
            scipy.io.wavfile.write(path, self.rate, data)
        return
