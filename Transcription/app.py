from tkinter import *
from gradio_client import Client
class myClient:
    def __init__(self, url, api_name):
        self.url = url
        self.api_name = api_name
        self.client = Client(self.url)
    def submit(self, index_token, audio, callback_fn):
        text = self.client.submit(index_token, audio, api_name=self.api_name, result_callbacks=callback_fn)
        return text

class slideButton(Button):
    def __init__(self, parent, on_off_imgs = ["assets/on.png", "assets/off.png"]):
        super(slideButton, self).__init__(parent)
        self.on_image = PhotoImage(file=on_off_imgs[0])
        self.off_image = PhotoImage(file=on_off_imgs[1])
        self.state_on = False
        self.config(image=self.off_image)
        self.config(command=self.command)
        self.config(border=0)
    def command(self):
        if self.state_on:
            self.config(image=self.off_image)
            self.state_on = False
        else:
            self.config(image=self.on_image)
            self.state_on = True

if __name__ =="__main__":
    pass
    # ws = Tk()
    # ws.title('Python Guides')
    # ws.geometry("400x300")
    # bt = slideButton(ws)
    # bt.pack()
    # ws.mainloop()





