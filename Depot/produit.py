from GestionDepot import *
from DBManagement import *

from tkinter import ttk

# class Produit
class Produit(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.AddProductFrame = Frame(self, bg="SeaGreen1")
        self.AddProductFrame.pack(side=LEFT)
        

        self.DeleteProductFrame = Frame(self, bg="SeaGreen1")
        self.DeleteProductFrame.pack(side= RIGHT)

        self.geometry('700x500')
        self.resizable(True,True)

        self.ViewFrame = Frame(self, bg="SeaGreen1")
        self.ViewFrame.pack(side=TOP)

        self.ModifyFrame = Frame(self, bg="SeaGreen1")
        self.ModifyFrame.pack(side=BOTTOM)

        # Produit database definition
        self.db = "./dbs/DBproduit.db"
        self.table = "produit"
        self.query = '''CREATE TABLE "produit" (
                    "productname"	string NOT NULL,
                    "prixachat"	float,
                    "prixvente"	float,
                    "description"	string NOT NULL,
                    "createdate"	datetime,
                    "Nombre" float,
                    "Benefice" float,
                    PRIMARY KEY("productname")
                );'''

        #Pretty table variables
        self.t = Text(self)
        self.x = PrettyTable()
    

        #self.geometry('900x500')
        self.resizable(height=None,width=None)
        self.title("Produits")


        self.dbm = DBManagement(self.db,self.table,"rowname","rowvalue",self.query)

        if(not self.dbm.Checkiftableexists()):
            self.dbm.CreateTable()

        

        # Add product widgets
        self.labelAddProduct = tk.Label(self.AddProductFrame, text="Add new Product", fg="blue", font="bold").pack(expand=True,ipady=0)
        self.productnamelabel = tk.Label(self.AddProductFrame, text="Name", fg="blue").pack(expand=True,ipady=0)
        self.productname = tk.Text(self.AddProductFrame,width=30,height=1, fg="blue")
        self.productname.pack(ipady=0)
        
        
        self.prixachatlabel = tk.Label(self.AddProductFrame, text="Prix achat", fg="blue").pack(expand=True,ipady=0)
        self.prixachat = tk.Text(self.AddProductFrame,width=30,height=1, fg="blue")
        self.prixachat.pack(ipady=0)

        self.prixventel = tk.Label(self.AddProductFrame, text="Prix vente", fg="blue").pack(expand=True,ipady=0)
        self.prixvente = tk.Text(self.AddProductFrame,width=30,height=1, fg="blue")
        self.prixvente.pack(ipady=0)

        self.descriptionlabel = tk.Label(self.AddProductFrame, text="description", fg="blue").pack(expand=True,ipady=0)
        self.description = tk.Text(self.AddProductFrame,width=30,height=1, fg="blue")
        self.description.pack(ipady=0)

         #Create a Label
        self.lbdatapicker = tk.Label(self.AddProductFrame, text= "Choose a Date", background= 'gray61', foreground="white").pack(ipady=0)
        #Create a Calendar using DateEntry
        self.cal = DateEntry(self.AddProductFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
        self.cal.pack(pady=10)

        self.insertbtn = tk.Button(self.AddProductFrame,
                text='Add Product', fg="blue",font = "Helvetica 10 bold italic",
                command=self.insertproduct).pack(expand=True,ipady=0)
        
        
        

        # Add Deleteproduct widgets
        self.labelDeleteProduct = tk.Label(self.DeleteProductFrame, text="Delete product", fg="blue", font="bold").pack(expand=True,ipady=0)
        self.productnamelabeldel = tk.Label(self.DeleteProductFrame, text="Name", fg="blue").pack(expand=True,ipady=0)

        self.productnamedel = Combobox(self.DeleteProductFrame, values= self.dbm.SelectColumn("productname",self.db,self.table,None))
        self.productnamedel['state'] = 'readonly'
        self.productnamedel.pack(pady=0)

        self.Deletebtn = tk.Button(self.DeleteProductFrame,
            text='Delete Product', fg="blue",font = "Helvetica 10 bold italic",
            command=self.Deleteproduct).pack(expand=True,ipady=0)
        
        #self.productnamemoddefault = ""
        
       
       # Add Modify produit 
        self.labelModifyProduct = tk.Label(self.ModifyFrame, text="Modifier le produit", fg="blue", font="bold").pack(expand=True,ipady=0)
        self.productnamelabelmod = tk.Label(self.ModifyFrame, text="Name", fg="blue").pack(expand=True,ipady=0)
        self.productnamemod = Combobox(self.ModifyFrame,values= self.dbm.SelectColumn("productname",self.db,self.table,None))
        self.productnamemod['state'] = 'readonly'
        self.productnamemod.pack(pady=0)
        self.prixachatlabelm = tk.Label(self.ModifyFrame, text="Prix achat", fg="blue").pack(expand=True,ipady=0)
        self.prixachatm = tk.Text(self.ModifyFrame, width=30,height=1, fg="blue")
        self.prixachatm.pack(ipady=0)

        self.prixventelm = tk.Label(self.ModifyFrame, text="Prix vente", fg="blue").pack(expand=True,ipady=0)
        self.prixventem = tk.Text(self.ModifyFrame,width=30,height=1, fg="blue")
        self.prixventem.pack(ipady=0)
        self.nombrem = tk.Label(self.ModifyFrame, text="Nombre", fg="blue").pack(expand=True,ipady=0)
        self.nombrem = tk.Text(self.ModifyFrame,width=30,height=1, fg="blue")
        self.nombrem.pack(ipady=0)
        self.beneficem = tk.Label(self.ModifyFrame, text="Benefice", fg="blue").pack(expand=True,ipady=0)
        self.beneficem = tk.Text(self.ModifyFrame,width=30,height=1, fg="blue")
        self.beneficem.pack(ipady=0)
        self.Modifybtn = tk.Button(self.ModifyFrame,
            text='Modifier le Produit', fg="blue",font = "Helvetica 10 bold italic",
            command=self.Modifyproduct).pack(expand=True,ipady=0)
        
        self.tree = ttk.Treeview(self, column=("id","productname","entrees","sorties","Date","description","[Transaction]","Prix"), show='headings', height=300)
        self.dbm = DBManagement(self.db,self.table,"rowname","rowvalue",self.query)
        
        
        
        self.ViewProduct()

        

        #self.configure(background='skyblue')
        self.configure(background='MediumAquamarine')

        # Bind event to treeview
        self.tree.bind("<<TreeviewSelect>>", self.getSelectedItem)


    def clearViewFrame(self):
         for widgets in self.ViewFrame.winfo_children():
            widgets.destroy()

    def Getproductprice(self):
        print("")


    def insertproduct(self):

        try:
            db = self.db
            connection1 = sqlite3.connect(db)
            productname = str(self.productname.get("1.0",'end-1c')) 
            prixachat = int(self.prixachat.get("1.0",'end-1c'))
            prixvente = int(self.prixvente.get("1.0",'end-1c'))
            description = str(self.description.get("1.0",'end-1c'))


            # check validity
            if(' ' in productname or productname==""):
                messagebox.showerror("Error","name invalid")
                return

            

            #date1 = self.cal.cget()
            
            connection1 = sqlite3.connect(db)
            cursor1 = connection1.cursor()
            cursor1.execute("insert into produit(productname,prixachat,prixvente,description,createdate) values (?,?,?,?,?)",(productname,prixachat,prixvente,description,self.cal.get_date()))
            connection1.commit()
            messagebox.showinfo(title="Add Product", message="Product  Sucessful added", icon="info")

            self.productnamedel['values'] = self.dbm.SelectColumn("productname",self.db,self.table,None)
            self.productnamemod['values'] = self.dbm.SelectColumn("productname",self.db,self.table,None)

            self.ViewProduct()
            
        except Exception as e:
            messagebox.showinfo(title="Exception", message=str(e), icon="error")
        finally:
            if connection1:
                connection1.close()
        #self.

    def Deleteproduct(self):

        try:
            db = self.db #"DBdepot.db"
            table = self.table #"produit"
            rowname = "productname"
            productname = str(self.productnamedel.get())
           
            
            connection1 = sqlite3.connect(db)

            self.dbm.rowname = rowname
            self.dbm.rowvalue =  productname
            self.dbm.deleteItem()
            #if(self.dbm.deleteItem()):
                #messagebox.showinfo(title="Delete Product", message="Product sucessful deleted", icon="info")

            # Update combox product.
            self.productnamedel['values'] = self.dbm.SelectColumn("productname",self.db,self.table,None)
            self.productnamemod['values'] = self.dbm.SelectColumn("productname",self.db,self.table,None)

            # Call View products after deletion
            self.ViewProduct()
            
        except Exception as e:
            messagebox.showinfo(title="Exception", message=str(e), icon="error")
        finally:
            if connection1:
                connection1.close()

    def Filltreeview(self,rows):
        
        #if(not bool(self.tree.winfo_ismapped())):
             # Add a Treeview widget
        i = 0
        self.tree.tag_configure("pair_row", background="SeaGreen1")
        self.tree.tag_configure("impair_row", background="MediumAquamarine")
            
        self.tree.column("# 1", anchor=CENTER)
        self.tree.heading("# 1", text="Productname")
        self.tree.column("# 2", anchor=CENTER)
        self.tree.heading("# 2", text="Prixachat")
        self.tree.column("# 3", anchor=CENTER)
        self.tree.heading("# 3", text="prixvente")
        self.tree.column("# 4", anchor=CENTER)
        self.tree.heading("# 4", text="description")
        self.tree.column("# 5", anchor=CENTER)
        self.tree.heading("# 5", text="Create Date")
        self.tree.column("# 6", anchor=CENTER)
        self.tree.heading("# 6", text="Nombre")
        self.tree.column("# 7", anchor=CENTER)
        self.tree.heading("# 7", text="Benefice")
        #self.tree.column("# 8", anchor=CENTER)
        #self.tree.heading("# 8", text="Prix")
        # Insert the data in self.treeview widget
        for row in rows:
            if(i%2):
                row = self.tree.insert('', 'end', text="1",values=row,tag="pair_row")
                i = i+1
            else:
                row= self.tree.insert('', 'end', text="1",values=row,tag="impair_row")
                i = i +1
        self.tree.pack()

    ''' View all available products'''
    def ViewProduct(self):
        # empty treeview
        for i in self.tree.get_children():
           self.tree.delete(i)

        rows = self.dbm.ViewTable()
        self.Filltreeview(rows)

    def Modifyproduct(self):
        nom = float(self.nombrem.get("1.0",'end-1c'))
        beneficem = float(self.beneficem.get("1.0",'end-1c'))
        self.dbm.UpdateColumn("productname","./dbs/DBproduit.db","produit",self.productnamemod.get(),"prixachat",self.prixachatm.get("1.0",'end-1c'))
        self.dbm.UpdateColumn("productname","./dbs/DBproduit.db","produit",self.productnamemod.get(),"prixvente",self.prixventem.get("1.0",'end-1c'))
        self.dbm.UpdateColumn("productname","./dbs/DBproduit.db","produit",self.productnamemod.get(),"Nombre",nom)
        self.dbm.UpdateColumn("productname","./dbs/DBproduit.db","produit",self.productnamemod.get(),"Benefice",beneficem)
        self.ViewProduct()

    def getSelectedItem(self,event):
        #print("Item selected")
        self.prixachatm.delete("1.0",END)
        self.prixventem.delete("1.0",END)
        self.nombrem.delete("1.0",END)
        self.beneficem.delete("1.0",END)

        selecteditem = self.tree.focus()
        selectvalues = self.tree.item(selecteditem)['values']
        #print(selectvalues[0])
        self.productnamemod.set(selectvalues[0])
        #self.productnamemoddefault = str(selectvalues[0])
        self.prixachatm.insert("1.0",str(selectvalues[1]))
        self.prixventem.insert("1.0",str(selectvalues[2]))
        self.nombrem.insert("1.0",str(selectvalues[5]))
        self.beneficem.insert("1.0",str(selectvalues[6]))
        

        

        
