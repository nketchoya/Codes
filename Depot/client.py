from GestionDepot import *
from DBManagement import *

# class Client
class Client(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

       # self.AddClientFrame = Frame(self, bg="cyan")
        self.AddClientFrame = Frame(self, bg="SeaGreen1")
        self.AddClientFrame.pack(side=LEFT)
        

        #self.DeleteClientFrame = Frame(self, bg="cyan")
        self.DeleteClientFrame = Frame(self, bg="SeaGreen1")
        self.DeleteClientFrame.pack(side= RIGHT)

       # self.ViewFrame = Frame(self, bg="cyan")
        self.ViewFrame = Frame(self, bg="SeaGreen1")
        self.ViewFrame.pack(side=TOP)

        #self.ModifyFrame = Frame(self, bg="cyan")
        self.ModifyFrame = Frame(self, bg="SeaGreen1")
        self.ModifyFrame.pack(side=BOTTOM)

        # Produit database definition
        self.db = "./dbs/DBClient.db"
        self.table = "Client"
        self.query = '''CREATE TABLE "Client" (
                    "clientname"	string NOT NULL,
                    "address"	string NOT NULL,
                    "description"	string NOT NULL,
                    "createdate"	datetime,
                    PRIMARY KEY("clientname")
                );'''

        #Pretty table variables
        self.t = Text(self)
        self.x = PrettyTable()

        self.geometry('700x500')
        self.title("Panel Clients")


        self.dbm = DBManagement(self.db,self.table,"rowname","rowvalue",self.query)

        if(not self.dbm.Checkiftableexists()):
            self.dbm.CreateTable()

        

        # Add client widgets
        self.labelAddclient = tk.Label(self.AddClientFrame, text="Add new client", fg="blue", font="bold").pack(expand=True,ipady=0)
        self.clientnamelabel = tk.Label(self.AddClientFrame, text="Name", fg="blue").pack(expand=True,ipady=0)
        self.clientname = tk.Text(self.AddClientFrame,width=30,height=1, fg="blue")
        self.clientname.pack(ipady=0)
        
    
        self.Addressl = tk.Label(self.AddClientFrame, text="Address", fg="blue").pack(expand=True,ipady=0)
        self.Address = tk.Text(self.AddClientFrame,width=30,height=1, fg="blue")
        self.Address.pack(ipady=0)

        self.descriptionlabel = tk.Label(self.AddClientFrame, text="description", fg="blue").pack(expand=True,ipady=0)
        self.description = tk.Text(self.AddClientFrame,width=30,height=1, fg="blue")
        self.description.pack(ipady=0)

         #Create a Label
        self.lbdatapicker = tk.Label(self.AddClientFrame, text= "Choose a Date", background= 'gray61', foreground="white").pack(ipady=0)
        #Create a Calendar using DateEntry
        self.cal = DateEntry(self.AddClientFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
        self.cal.pack(pady=10)

        self.insertbtn = tk.Button(self.AddClientFrame,
                text='Add client', fg="blue",font = "Helvetica 10 bold italic",
                command=self.insertclient).pack(expand=True,ipady=0)
        
        
        

        # Add Deleteclient widgets
        self.labelDeleteclient = tk.Label(self.DeleteClientFrame, text="Delete client", fg="blue", font="bold").pack(expand=True,ipady=0)
        self.clientnamelabeldel = tk.Label(self.DeleteClientFrame, text="Name", fg="blue").pack(expand=True,ipady=0)

        self.clientnamedel = Combobox(self.DeleteClientFrame, values= self.dbm.SelectColumn("clientname",self.db,self.table,None))
        self.clientnamedel['state'] = 'readonly'
        self.clientnamedel.pack(pady=0)

        self.Deletebtn = tk.Button(self.DeleteClientFrame,
            text='Delete client', fg="blue",font = "Helvetica 10 bold italic",
            command=self.Deleteclient).pack(expand=True,ipady=0)

        
       # Add Modify produit 
        self.labelModifyclient = tk.Label(self.ModifyFrame, text="Update Client", fg="blue", font="bold").pack(expand=True,ipady=0)
        self.clientnamelabelmod = tk.Label(self.ModifyFrame, text="Name", fg="blue").pack(expand=True,ipady=0)
        self.clientnamemod = Combobox(self.ModifyFrame, values= self.dbm.SelectColumn("clientname",self.db,self.table,None))
        self.clientnamemod['state'] = 'readonly'
        self.clientnamemod.pack(pady=0)
        

        self.Addresslm = tk.Label(self.ModifyFrame, text="Address", fg="blue").pack(expand=True,ipady=0)
        self.Addressm = tk.Text(self.ModifyFrame,width=30,height=1, fg="blue")
        self.Addressm.pack(ipady=0)
        self.Modifybtn = tk.Button(self.ModifyFrame,
            text='Update Client', fg="blue",font = "Helvetica 10 bold italic",
            command=self.Modifyclient).pack(expand=True,ipady=0)
        
        
        
        self.Viewclient()

        

        #self.configure(background='skyblue')
        self.configure(background='MediumAquamarine')
        


    def clearViewFrame(self):
         for widgets in self.ViewFrame.winfo_children():
            widgets.destroy()


    def insertclient(self):

        try:
            db = self.db
            connection1 = sqlite3.connect(db)
            clientname = str(self.clientname.get("1.0",'end-1c')) 
            address = str(self.Address.get("1.0",'end-1c'))
            description = str(self.description.get("1.0",'end-1c'))

            # check validity
            if(' ' in clientname or clientname==""):
                messagebox.showerror("Error","name invalid")
                return
            
            connection1 = sqlite3.connect(db)
            cursor1 = connection1.cursor()
            cursor1.execute("insert into Client(clientname,address,description,createdate) values (?,?,?,?)",(clientname,address,description,self.cal.get_date()))
            connection1.commit()
            messagebox.showinfo(title="Add client", message="client  Sucessful added", icon="info")

            self.clientnamedel['values'] = self.dbm.SelectColumn("clientname",self.db,self.table,None)
            self.clientnamemod['values'] = self.dbm.SelectColumn("clientname",self.db,self.table,None)

            self.Viewclient()
            
        except Exception as e:
            messagebox.showinfo(title="Exception", message=str(e), icon="error")
        finally:
            if connection1:
                connection1.close()
        #self.

    def Deleteclient(self):

        try:
            db = self.db #"DBdepot.db"
            table = self.table #"produit"
            rowname = "clientname"
            clientname = str(self.clientnamedel.get())
           
            
            connection1 = sqlite3.connect(db)

            self.dbm.rowname = rowname
            self.dbm.rowvalue =  clientname
            #self.dbm.deleteItem()
            if(self.dbm.deleteItem()):
                messagebox.showinfo(title="Delete client", message="client sucessful deleted", icon="info")

            # Call View clients after deletion
            self.Viewclient()
            
        except Exception as e:
            messagebox.showinfo(title="Exception", message=str(e), icon="error")
        finally:
            if connection1:
                connection1.close()


    ''' View all available clients'''
    def Viewclient(self):
        
        #self.clearViewFrame()
        if( not bool(self.t.winfo_ismapped())):
            #self.t.pack_forget()
            self.t = Text(self)
        else:
            self.t.delete("1.0", "end")
            #self.quit()
             
        self.x.clear_rows()
        self.x.field_names = ["clientname","Address","description","createdate"]
        rows = self.dbm.ViewTable()
        self.x.add_rows(rows)

        # Show table.
        self.t.insert(INSERT,self.x)
        self.t.pack()

    def Modifyclient(self):
        if(self.dbm.UpdateColumn("clientname","./dbs/DBClient.db","Client",self.clientnamemod.get(),"address",self.Addressm.get("1.0",'end-1c'))):
        # Call View clients after Modification
            self.Viewclient()
       # self.Viewclient()
        
