'''from tkPDFViewer import tkPDFViewer as pdf
from tkinter import*
root = Tk()

#create object like this.
variable1 = pdf.ShowPdf()
#Add your pdf location and width and height.
variable2 = variable1.pdf_view(root,pdf_location= "testfacture.pdf",width=50,height=100)
variable2.pack()
root.mainloop()'''

from datetime import date

today = date.today()

ym = str(today.year) + "-" + str(today.month)

print(ym)