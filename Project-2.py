import math
import cv2 as cv 
import numpy as np
import tkinter
import customtkinter
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from Crypto.Cipher import AES
import base64


#the GUI start
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


def encrypt_aes(message, key):
    # Pad the message to a multiple of 16 bytes
    padded_message = message + (AES.block_size - len(message) % AES.block_size) * chr(AES.block_size - len(message) % AES.block_size)
    # Create an AES cipher object with the key
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    # Encrypt the message and encode as base64
    encrypted_message = base64.b64encode(cipher.encrypt(padded_message.encode())).decode()
    return encrypted_message

def decrypt_aes(encrypted_message, key):
    # Decode the base64 encoded message
    ciphertext = base64.b64decode(encrypted_message.encode())
    # Create an AES cipher object with the key
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    # Decrypt the message and remove padding
    decrypted_message = cipher.decrypt(ciphertext).decode()
    decrypted_message = decrypted_message[:-ord(decrypted_message[-1])]
    return decrypted_message

 
    
def decode():    
     #The  input of image 
    imge_path = filedialog.askopenfilename()
      
    

    img = cv.imread(imge_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img_str = np.reshape(img, (np.product(img.shape)))

    text = ""

    for i in range(int(len(img_str)/8)):
            bit = img_str[8*i:8*(i+1)]
            #print(bit.shape)
            #print(bit)
            bit = np.remainder(bit, 2)
            #print(bit.shape)
            #print(bit)
            bit = ''.join(map(str, bit))
            #print(bit)

            ascii_character = chr(int(bit, 2))
            #print(ascii_character)
            if ascii_character == '~' :
                break
            else:
                text = text + ascii_character
            i+=8
    hidden_message1 = decrypt_aes(text, "446673bwe1far355")

    label = customtkinter.CTkLabel(master=app, text=hidden_message1)
    label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER) 

    label = customtkinter.CTkLabel(master=app, text=text)
    label.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER) 



def encode():

   #the GUI input of message 
    dialog = customtkinter.CTkInputDialog(text="Type in the hidden message " , title="Hidden message")
    text=dialog.get_input()  

    encrypted_message = encrypt_aes(text, "446673bwe1far355")
       
    #The  input of image path
    imge_path = filedialog.askopenfilename()
    
    img = cv.imread(imge_path)
    pil_img2 = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))

    #Showing image before hide
    image = pil_img2.resize((350, 250))
    photo = ImageTk.PhotoImage(image)
    labe4.configure(image=photo)
    labe4.image = photo

    

    limit = math.floor(img.shape[0]*img.shape[1]*img.shape[2]-8)/8

    if len(encrypted_message) <= (img.shape[0]*img.shape[1]*img.shape[2]-8)/8 :

            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img_str = np.reshape(img, (np.product(img.shape)))

            bit_str=""
            a = ' '.join(format(ord(x), 'b') for x in encrypted_message)
            LL = list(a.split(' '))
            for i, bit in enumerate(LL):
                bit_str = bit_str + bit.zfill(8)

            bit_str = bit_str + "01111110"
            #print(bit_str)

            for i in range(len(bit_str)):
                #print(bit_str[i],img_str[i])

                if bit_str[i] == '0':
                    if img_str[i]%2 != 0:

                        img_str[i] = img_str[i] + 1
                    #print(bit_str[i],img_str[i])
                else:
                    if img_str[i]%2 == 0:

                        img_str[i] = img_str[i] + 1
                    #print(bit_str[i],img_str[i])

            final_image = np.reshape(img_str , img.shape)

            cv.imwrite("cover0.png", cv.cvtColor(final_image, cv.COLOR_RGB2BGR))
            print(r"Encoded image is saved as 'cover.png'")

             
            #showing image after hiding
            pil_img = Image.fromarray(final_image)
            image = pil_img.resize((350, 250))
            photo = ImageTk.PhotoImage(image)
            labe3.configure(image=photo)
            labe3.image = photo   

            #the mse part
            img1 = np.array(Image.open(imge_path))
            img2 = np.array(Image.open("cover0.png"))

            
            mse = np.mean((img1 - img2) ** 2)  
            print(mse)
            labe7 = customtkinter.CTkLabel(master=app, text="MSE",text_color=("#3996D5"))
            labe7.place(relx=0.36, rely=0.5, anchor=tkinter.CENTER) 

            labe5 = customtkinter.CTkLabel(master=app, text= mse)
            labe5.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER) 
           

            return final_image
           

            

    else:
            print("Try again with higher resolution image!\nNo.of characters to encode exceed maximum capacity of the image\n")
            print("\nMaximum Characters allowed are : ",limit)
            
            return None
        

# create CTk window 
app = customtkinter.CTk()  
app.geometry(f"{800}x{600}")
app.title("Steganography")

       
labe2 = customtkinter.CTkLabel(master=app, text="Steganogrphy", width= 150,height=70,font=(super,35),text_color=("#3996D5"))
labe2.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="Encoding", command= encode)
button.place(relx=0.3, rely=0.3, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="Decoding", command= decode)
button.place(relx=0.7, rely=0.3, anchor=tkinter.CENTER)



# create CTkLabel widgets for displaying the images
labe3 = customtkinter.CTkLabel(master=app, text="")
labe3.place(relx=0.3, rely=0.7, anchor=customtkinter.CENTER)


labe4 = customtkinter.CTkLabel(master=app, text="")
labe4.place(relx=0.7, rely=0.7, anchor=customtkinter.CENTER)

labe2 = customtkinter.CTkLabel(master=app, text="Before Hidding", width= 150,height=60,font=(super,20),text_color=("#3996D5"))
labe2.place(relx=0.7, rely=0.93, anchor=tkinter.CENTER)

labe2 = customtkinter.CTkLabel(master=app, text="After Hidding", width= 150,height=60,font=(super,20),text_color=("#3996D5"))
labe2.place(relx=0.3, rely=0.93, anchor=tkinter.CENTER)


app.mainloop()