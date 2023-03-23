from datetime import date
from msilib.schema import Icon
from optparse import Values
import string
from tkinter import * 
import sqlite3
from sqlite3 import Error
import os, glob
from turtle import position, up, width
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from tkinter.ttk import Combobox

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tkcalendar import *


from prettytable import PrettyTable

from DBManagement import *
from produit import *
from client import *
from transactions import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

       

        # Menu
        menu = tk.Menu(self)
        submenu = tk.Menu(menu, tearoff=0)
        submenu.add_separator()
        menu.add_cascade(label="File", menu=submenu)
        submenu.add_cascade(label="Client", command=self.Client) 
        submenu.add_cascade(label="Produit", command=self.Produit) 
        submenu.add_cascade(label="Transaction", command=self.Transactions) 
       # submenu.add_cascade(label="Facture", command=self.Facture) 
        submenu.add_cascade(label="Quit", command=self.destroy) 
       # menu.add_command(label="View stocks", command=self.ViewStocks)     
        menu.add_command(label="About", command=self.About)
        self.config(menu=menu)
        self.resizable(True,True)
        self.geometry('1000x600')

         
    def access_bilan(choice):
        return
        #choice = variable.get()

    def About(self):
        messagebox.showinfo("About", "Depot will help you manage small project ..enjoy.. Germain.. 01.2023")
        return  

                                                                                      

    def bilans(self):
        mylist = []
        applicationfolder = os.getcwd()
        os.chdir(applicationfolder)
        for file in glob.glob("*.db"):
            file1 = file.split(".")
            mylist.append(file1[0])
            #print(file)
        return mylist

    
    def create_table(self,conn):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        sql_create_bilan_table = """ create table "Product" (
	"id"	integer,
	"productname"	string NOT NULL,
	"entress"	integer,
	"sorties"	integer,
	"createdate"	datetime,
	"description"	string NOT NULL,
	PRIMARY KEY("id")
); """

        try:
            c = conn.cursor()
            c.execute(sql_create_bilan_table)
        except Error as e:
            print(e)

    
    def createDatabase(self):
        
        try:
            bilan = str(self.text.get("1.0",'end-1c'))
            dbname =  bilan + ".db"
            currentdirectory = os.getcwd()
            pathtofile = currentdirectory + "\\" + dbname
            print(os.path.exists(pathtofile))
            if(os.path.exists(pathtofile)):
                messagebox.showerror("Error","La Bilan " + bilan + " existe deja")
                self.text.delete("1.0",'end-1c')
                return
            else:
                connection = sqlite3.connect(dbname)
                messagebox.showinfo("Bilan Creation","le Bilan  "+ bilan + " a été créé")
                self.text.delete("1.0",'end-1c')
                self.cb['values'] = self.bilans()  # refresh bilan combox here
                self.create_table(connection)
                connection.close()
        except Exception as e:
            #print(e)
            messagebox.showerror("Error",str(e))
            connection.rollback()
        #finally:
        #   connection.cursor()
        #  connection.close()

    # Update specific stock Item
    def OpenDataBase(self):
        window = Window(self)
        window.grab_set()
    
    #View actual Items in stock
    #def Facture(self):
     #   facture = Facture(self)
      #  facture.grab_set()

    #View actual Items in stock
    def Client(self):
        client = Client(self)
        #client.grab_set()

     #View actual Items in stock
    def Produit(self):
        produit = Produit(self)
        #produit.grab_set()

     #View actual Items in stock
    def Transactions(self):
        transaction1 = Transaction(self)
        #transaction1.grab_set()




    def DeleteBilan(self):
        yesorno = messagebox.askquestion("Delete transaction","Do you really want to delete transaction " + str(self.cbDelete.get()))
        if(yesorno == "yes"):
            todeltebilan = str(self.cbDelete.get()) + ".db"
            os.remove(todeltebilan)
            self.cb['values'] = self.bilans()  # refresh bilan combox here
            self.cbDelete['values'] = self.bilans()  # refresh bilan combox here
            messagebox.showinfo("Deletion Info",str(self.cbDelete.get()) + " deleted")
          

if __name__ == "__main__":
    app = App()
    app.title("Depot v 1.0")
    #app.configure(background='#AFAFEE')
    #app.configure(background='skyblue')
    app.configure(background='MediumAquamarine')
    #app.resizable(0,0)
    #app.bg
    app.mainloop()