import tkinter as tk
from tkinter import messagebox
import base64Images
class InfixToPostfixConverter:
    def __init__(self):
        self.window = tk.Tk()
        # Setting the dimension of the application
        self.window.geometry("1270x600")
        # Setting the background color of GUI
        self.window.config(bg="#f8c291")
        # Setting the title of GUI
        self.window.title("Infix to Postfix Converter")
        # Disable resizing the GUI
        self.window.resizable(False,False)
        # Base64 pictures converted to PhotoImage
        self.appIconPicture = tk.PhotoImage(data=base64Images.base64Images.appIcon)
        self.convertPicture = tk.PhotoImage(data=base64Images.base64Images.convertIcon)
        self.copyIconPicture = tk.PhotoImage(data=base64Images.base64Images.copyIcon)
        # Frame
        self.frame = tk.Frame(self.window,bg="#f8c291")
        self.frame.pack(pady=20)
        # Label
        self.info=tk.Label(self.frame,text="Enter infix expression here:",fg="black",font=("Times New Roman",14),bg="#f8c291")
        self.info.pack()
        # StringVar to store value
        self.expr = tk.StringVar(self.window)
        #  Entry box to get input from user
        self.entry = tk.Entry(self.frame,font=("Helvetica",17),width=40)
        self.entry.pack()
        # Enabling copy in Entry
        self.entry.event_generate("<<Copy>>")
        # Enabling paste in Entry
        self.entry.event_generate("<<Paste>>")
        # Submit button to convert and display conversion process step by step in Listbox 'listbox1' with inner padding 7.
        self.submitBtn = tk.Button(self.frame,text="Convert",command=self.infixToPostfix,bg="#eb2f06",fg="white",font=("Arial",18,"bold"),activebackground="#EB2F06",padx=8)
        self.submitBtn.pack(pady=9)
        self.submitBtn.config(image=self.convertPicture,compound=tk.LEFT)
        # IntVar
        self.fullPostfixFinal = tk.StringVar()
        # Label to display the finally converted postfix expression
        self.resultLabel = tk.Label(self.frame,textvariable=self.expr,font=("Arial",18),bg="#ffc6a5",wraplength=400)
        self.resultLabel.pack()
        # Button to copy the full final postfix string generated
        self.copyPostfixButton = tk.Button(self.frame,text="Copy full postfix expression",command=self.copyPostfixExpression,bg="#b71540",fg="yellow",activebackground="#b71540",font=("Times New Roman",13),image=self.copyIconPicture,compound=tk.LEFT,padx=7)
        self.copyPostfixButton.pack()
        # Frame
        self.frame1 = tk.Frame(self.window,bg="#f8c291")
        self.frame1.pack(padx=30,pady=3)
        # Vertical scroll bar
        self.yscrollbar = tk.Scrollbar(self.frame1)
        self.yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        # Listbox to display the conversion process step by step
        self.listbox1 = tk.Listbox(self.frame1,yscrollcommand=self.yscrollbar.set,width=0,font=("Arial",14),activestyle="none")
        self.listbox1.pack(fill="both",expand=tk.YES)
        # Attaching the vertical scroll bar to the Listbox 'listbox1'
        self.yscrollbar.config(command = self.listbox1.yview)
        # Button to copy the displayed content inside the Listbox 'listbox1'.
        self.copyBtn = tk.Button(self.window,text="Copy to clipboard",command=self.copyContentOfListbox,bg="#b71540",font=("Times New Roman",13),fg="white",activebackground="#b71540",image=self.copyIconPicture,compound=tk.LEFT,padx=7)
        self.copyBtn.pack(pady=7)
        # Initially hide the Listbox 'listbox1'
        self.hideListbox()
        self.window.iconphoto(True,self.appIconPicture)
        self.window.mainloop()

    # Function to convert the user input infix expression to postfix expression and to display conversion in LIstbox

    def infixToPostfix(self):
        # Delete all items from listbox
        self.listbox1.delete(0, tk.END)
        # Get the user input infix expression from the Entry 'entry'
        infix = self.entry.get()
        if self.isProperInfixExpression()==True:
            # show the listbox
            self.showListbox()
            postfix = ""
            precedenceMap = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
            stack = []
            topPtr = -1
            ptr = 0
            while ptr < len(infix):
                ch = infix[ptr]
                if ch not in "+-*/^()":
                    postfix += ch
                else:
                    if topPtr == -1:
                        stack.append(ch)
                        topPtr += 1
                    else:
                        if ch == "(":
                            stack.append(ch)
                            topPtr += 1
                        elif ch == ")":
                            while topPtr >= 0 and stack[topPtr] != "(":
                                postfix += stack.pop()
                                topPtr -= 1
                            stack.pop()
                            topPtr -= 1
                        elif ch in "+-*/^":
                            if stack[topPtr] == "(":
                                stack.append(ch)
                                topPtr += 1
                            elif precedenceMap.get(stack[topPtr]) < precedenceMap.get(ch):
                                stack.append(ch)
                                topPtr += 1
                            elif precedenceMap.get(stack[topPtr]) > precedenceMap.get(ch):
                                postfix += stack.pop()
                                topPtr -= 1
                                ptr = ptr - 1
                            elif precedenceMap.get(stack[topPtr]) == precedenceMap.get(ch):
                                postfix += stack.pop()
                                topPtr -= 1
                                stack.append(ch)
                                topPtr += 1
                result = "Stack=" + str(stack) + "     Postfix=" + postfix
                self.listbox1.insert(self.listbox1.size(), result)
                ptr += 1
            while topPtr >= 0:
                postfix += stack.pop()
                topPtr -= 1
                result = "Stack=" + str(stack) + "     Postfix=" + postfix
                self.listbox1.insert(self.listbox1.size(), result)
            self.fullPostfixFinal.set(postfix)
            if len(postfix)>50:
                self.expr.set(postfix[:50]+"..............")
            else:
                self.expr.set(postfix)
        else:
            # Hide the listbox, label 'resultLabel' and copy buttons
            self.hideListbox()
            # Warns user with mistakes in the user input infix expression
            messagebox.showwarning("Warning", "Invalid infix expression\nPlease enter a valid infix expression without spaces")

    # Function to hide the listbox along with copy buttons, scrollbar, and resultLabel
    def hideListbox(self):
        self.resultLabel.pack_forget()
        self.copyPostfixButton.pack_forget()
        self.listbox1.pack_forget()
        self.yscrollbar.pack_forget()
        self.copyBtn.pack_forget()

    # Function to show the listbox along with copy buttons, scrollbar, and resultLabel

    def showListbox(self):
        self.resultLabel.pack()
        self.copyPostfixButton.pack()
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox1.pack()
        self.copyBtn.pack()

    # Function to copy all the step by step conversions displayed in the listbox to the clipboard to paste anywhere else.
    def copyContentOfListbox(self):
        self.window.clipboard_clear()
        selected = self.listbox1.get(0, self.listbox1.size())
        self.window.clipboard_append(selected)
        
    # Function to copy the final postfix expression fully to the clipboard
    def copyPostfixExpression(self):
        self.window.clipboard_clear()
        selected = self.fullPostfixFinal.get()
        self.window.clipboard_append(selected)

    # Function to check if the user input infix expression is invalid with empty string or white spaces or not.
    def isProperInfixExpression(self):
        if self.entry.get()=="" or self.entry.get().find(" ")>=0:
            return False
        return True
InfixToPostfixConverter()