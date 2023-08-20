import customtkinter
from PIL import Image

def slider_event(value):
  volVal = value
  print(volVal)
  if volVal < 25:
    my_image.configure(light_image=Image.open("CTkRangeSlider-main/Images/Zero.png"), size=(150,125)) 

  elif volVal < 75 and volVal > 25:
    my_image.configure(light_image=Image.open("VolumeButtons/Min.png"), size=(150,125)) 

  elif volVal < 100 and volVal > 75:
    my_image.configure(light_image=Image.open("VolumeButtons/More.png"), size=(150,125)) 

  elif volVal < 150 and volVal > 100:
    my_image.configure(light_image=Image.open("VolumeButtons/Max.png"), size=(150,125)) 

customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.title("Volume")
app.geometry("250x210+830+680")

slider = customtkinter.CTkSlider(app, from_=0, to=150, command=slider_event)

my_image = customtkinter.CTkImage(light_image=Image.open("VolumeButtons/Min.png"), size=(150,125)) 
image_label = customtkinter.CTkLabel(app, image=my_image, text="")

slider.grid(row=1, column=0, padx=20, pady=15)
image_label.grid(row=0, column=0, padx=50, pady=10)

app.mainloop()