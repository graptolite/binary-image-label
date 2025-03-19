#!/usr/bin/env python3

'''
Binary-Choice Image Labeller GUI | Label directory containing images (.png's).
    Copyright (C) 2025 Yingbo Li

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from tkinter import *
from PIL import Image,ImageTk
import os

class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x900")
        self.title("Binary Labeller")
        self.inputs_frame = Frame(self,bg="lightgrey",borderwidth=5)
        self.inputs_frame.columnconfigure(0,weight=1)
        self.inputs_frame.columnconfigure(0,weight=3)
        self.inputs_frame.place(relheight=1,relwidth=0.3,relx=0.7,y=0)
        self.l_input = Label(self.inputs_frame,text="Input Filepath:",font=("bold"))
        self.inp = Entry(self.inputs_frame)
        self.btn = Button(self.inputs_frame,text="Load files",width=10,height=5,command=self.load_files)

        input_widget_list = [self.l_input,self.inp,self.btn]
        self.stack_widgets(input_widget_list)

        self.bind("<Down>",lambda event=None : self.label("n"))
        self.bind("<Up>",lambda event=None : self.label("y"))
        self.bind("<Return>",lambda event=None : self.rename())

        self.outputs_frame = Frame(self,bg="lightblue",borderwidth=5)
        self.outputs_frame.columnconfigure(0,weight=1)
        self.outputs_frame.columnconfigure(0,weight=3)
        self.outputs_frame.place(relheight=1,relwidth=0.7,relx=0,y=0)

        self.l_output = Label(self.outputs_frame,text="Image",bg="lightblue")
        self.update_idletasks()
        w,h = self.outputs_frame.winfo_width(),self.outputs_frame.winfo_height()
        self.canv = Canvas(self.outputs_frame,width=0.9*w,height=0.6*h,bg="white")

        self.l_msg = Label(self.outputs_frame,text="Messages",bg="lightblue")
        self.msg = Canvas(self.outputs_frame,width=0.9*w,height=0.2*h,bg="white")

        output_widget_list = [self.l_output,self.canv,self.l_msg,self.msg]
        self.stack_widgets(output_widget_list)

        self.update_idletasks()
        wc,hc = self.canv.winfo_width(),self.canv.winfo_height()
        self.img_placeholder = self.canv.create_image(wc/2,hc/2,anchor=CENTER)
        wm,hm = self.msg.winfo_width(),self.msg.winfo_height()
        self.text_placeholder = self.msg.create_text(wm/2,hm/2,anchor=CENTER)

        self.protocol("WM_DELETE_WINDOW",self.destroy)
        self.fp = ""
        self.files = []
        self.counter = 0
        self.full_len = 0
        self.new_file = "new_file"
        self.active_file = "active_file"
        return
    def load_files(self):
        fp = self.inp.get()
        self.fp = fp
        if fp and os.path.exists(fp):
            print("a")
            self.files = [f for f in os.listdir(fp) if f.endswith(".png")]
            self.full_len = len(self.files)
            self.active_file = self.files[0]
            self.display_image()
        if not os.path.exists(os.path.join(self.fp,"Y")):
            os.mkdir(os.path.join(self.fp,"Y"))
        if not os.path.exists(os.path.join(self.fp,"N")):
            os.mkdir(os.path.join(self.fp,"N"))
        return
    def label(self,label):
        self.new_file = os.path.join(label.title(),label.title() + self.active_file)
        self.update_msg("Labelling as " + self.new_file)
        return
    def rename(self):
        if os.path.basename(self.new_file)[1:] == os.path.basename(self.active_file):
            os.rename(os.path.join(self.fp,self.active_file),os.path.join(self.fp,self.new_file))
            self.counter += 1
            self.files.pop(0)
            if len(self.files):
                self.active_file = self.files[0]
                self.display_image()
                self.update_msg("Labelled (%s/%s) and loaded next file" % (self.counter,self.full_len))
            else:
                self.update_msg("Labelled (%s/%s) and loaded next file and FINISHED" % (self.counter,self.full_len))
        else:
            self.update_msg("No label provided - press up for a positive label (Y) and down for a negative (N)")
        return
    def stack_widgets(self,widget_list):
        for i,w in enumerate(widget_list):
            w.grid(column=0,row=0+i)
        return
    def display_image(self):
        w = int(1*self.canv.winfo_width())
        h = int(1*self.canv.winfo_height())
        img = Image.open(os.path.join(self.fp,self.active_file))
        img_w,img_h = img.size
        scale_w = w/img_w
        scale_h = h/img_h
        scale = min([scale_w,scale_h])
        self.img = ImageTk.PhotoImage(image=img.resize((int(img_w*scale),int(img_h*scale))))
        self.update_msg("Image displayed")
        self.update_canv(self.img)
        return
    def update_msg(self,text):
        self.msg.itemconfig(self.text_placeholder,text=text)
    def update_canv(self,img):
        self.canv.itemconfig(self.img_placeholder,image=img)


if __name__=="__main__":
    root = GUI()
    root.mainloop()
