import gradio as gr
import os
def logAudio_name(index_token,audio):
    print(f" index: {index_token}, audio: {audio}")
    return index_token, audio
text_in = gr.Text(visible=False)
audio_in = gr.Audio(source="microphone", type="filepath", visible=True)
text_out_1 = gr.Text(visible=False)
text_out_2 = gr.TextArea(visible=True)
app = gr.Interface(
    title= "Whisper speech recognition server",
    fn=logAudio_name,
    inputs= 
    [   text_in,
        audio_in
    ],
    outputs=[text_out_1, text_out_2],
    allow_flagging="never",
).launch(server_name='0.0.0.0')