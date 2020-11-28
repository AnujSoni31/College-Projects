import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.geometry('200x160')

def encrypt_image():
	file1 = filedialog.askopenfile(mode='r', filetype=[('jpg file', '*.jpg'), ('jpeg file', '*.jpeg'), ('png file', '*.png')])
	if file1 is not None:
		fileName = file1.name
		key = entry1.get(1.0, tk.END)
		fi = open(fileName, 'rb')
		image = fi.read()
		fi.close()
		image = bytearray(image)
		for index, values in enumerate(image):
			image[index] = values^int(key)
		fi1 = open(fileName, 'wb')
		fi1.write(image)
		fi1.close()


b1 = tk.Button(root, text='Encrypt/Decrypt', command=encrypt_image)
b1.place(x=45, y=10)

entry1 = tk.Text(root, height=1, width=10)
entry1.place(x=50, y=50)

root.mainloop()