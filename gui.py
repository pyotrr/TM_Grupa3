import tkinter.filedialog
import tkinter as tk


_height = 600
_width = 800


def select_file_from_modal(event, clicked_input):
    current_input_value = clicked_input.get()
    clicked_input.delete(0, len(current_input_value))
    path = tk.filedialog.askopenfilename(filetypes=[('WAV Files', '*.wav;*.WAV')])
    clicked_input.insert(0, path)
    return


def load_file(event, path, selected_file):
    import scipy.io.wavfile
    rate, data = scipy.io.wavfile.read(path)
    selected_file = data
    return


window = tk.Tk()

canvas = tk.Canvas(window, height=_height, width=_width, bg='#b8cbe6')
canvas.pack()
frame = tk.Frame(window)
frame.place(relwidth=0.8, relheight=0.05, relx=0.1, rely=0.1)


path_input = tk.Entry(frame)
path_input.place(relwidth=0.9, relheight=1)
path_input.insert(0, 'Select file...')
path_input.bind('<Button-1>', lambda event, clicked_input=path_input: select_file_from_modal(event, clicked_input))

audio_file = None
path_button = tk.Button(frame, text='Open')
path_button.place(relwidth=0.1, relheight=1, relx=0.9)
path_button.bind('<Button-1>', lambda event, selected_file=audio_file: load_file(event, path_input.get(), selected_file))