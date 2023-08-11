from customtkinter import *
from PIL import Image
import logic

root = CTk()
root.geometry('580x500')
root.title("Spotify to Mp3")
root.resizable(False,False)

bg = CTkImage(Image.open("music.png"), size = (580,500))

photo_label = CTkLabel(root, image= bg, text = "")
photo_label.place(x = 0, y = 0, relheight = 1, relwidth = 1)

label = CTkLabel(root, text= "Spotify to MP3", font= ("helvetica",40))
label.place(x = 120, y = 175)

filename_field = CTkEntry(root, width=290, height= 28)
filename_field.place(x = 110, y = 235)

convert = CTkButton(root, text = "Convert", command= lambda : logic.convert(filename_field.get()))
convert.place(x = 420, y = 234)

root.mainloop()

