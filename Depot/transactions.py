from GestionDepot import *
from DBManagement import *
from produit import *
from datetime import datetime
from datetime import date

from tkinter import ttk
from fpdf import FPDF
from tkPDFViewer import tkPDFViewer as pdfviewer

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages



# class for view stocks
class Transaction(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.AddTransactionFrame = Frame(self, bg="SeaGreen1")
        self.AddTransactionFrame.pack(side=BOTTOM)

        self.FilterTransactionFrame = Frame(self, bg="SeaGreen1")
        self.FilterTransactionFrame.pack(side=LEFT)

        self.FactureFrame = Frame(self, bg="SeaGreen1")
        self.FactureFrame.pack(side=RIGHT)

        self.sepratFrame = Frame(self.FactureFrame, bg="SeaGreen1")
        self.sepratFrame.pack(side=TOP)

        self.DeleteTransactionFrame =Frame(self.FactureFrame, bg="SeaGreen1")
        self.DeleteTransactionFrame.pack(side=BOTTOM)
        
        today = date.today()

        ym = str(today.year) + "-" + str(today.month)
        # database definition
        self.db = "./dbs/DBTransaction" + ym + ".db"

  
        

        self.table = "Transaktionen"
        self.query = '''create TABLE "Transaktionen" (
	"id"	integer,
	"productname"	string NOT NULL,
	"entress"	float,
	"sorties"	float,
	"createdate"	datetime,
	"description"	string,
    "prixtransaction" float,
	"Transaktionen"	string NOT NULL,
    "Benefice" float,
	PRIMARY KEY("id")
);'''

        #Pretty table variables
        #self.t = Text(self)
        #self.x = PrettyTable()
        

        self.geometry('700x500')
        self.title("Panel Transactions")

        self.tree = ttk.Treeview(self, column=("id","productname","entrees","sorties","Date","description","Transaktionen","Prix","Benefice"), show='headings', height=30)
        self.dbm = DBManagement(self.db,self.table,"rowname","rowvalue",self.query)

        if(not self.dbm.Checkiftableexists()):
            self.dbm.CreateTable()

        

        # Add Transaction widgets
        self.labelAddTransaction = tk.Label(self.AddTransactionFrame, text="Add new Transaction", fg="blue", font="bold").pack(expand=True,ipady=0)
        self.clientlabel = tk.Label(self.AddTransactionFrame, text="Client", fg="blue").pack(expand=True,ipady=0)
        self.client = Combobox(self.AddTransactionFrame, values= self.dbm.SelectColumn("clientname","./dbs/DBClient.db","Client",None))
        self.client['state'] = 'readonly'
        #self.client = tk.Text(self.AddTransactionFrame,width=30,height=1, fg="blue")
        self.client.pack(ipady=0)
        self.Transactionnamelabel = tk.Label(self.AddTransactionFrame, text="Choisir le produit", fg="blue").pack(expand=True,ipady=0)
        #self.productname = tk.Text(self.AddTransactionFrame,width=30,height=1, fg="blue")
        self.productname = Combobox(self.AddTransactionFrame, values= self.dbm.SelectColumn("productname","./dbs/DBproduit.db","produit",None))
        self.productname['state'] = 'readonly'
        self.productname.pack(ipady=0)
        self.entreelabel = tk.Label(self.AddTransactionFrame, text="acheter", fg="blue").pack(expand=True,ipady=0)
        self.entree = tk.Text(self.AddTransactionFrame,width=30,height=1, fg="blue")
        self.entree.pack(ipady=0)
        #self.text1 = tk.Text(self, height=1, width=50)
        self.sortielabel = tk.Label(self.AddTransactionFrame, text="vendre", fg="blue").pack(expand=True,ipady=0)
        self.sortie = tk.Text(self.AddTransactionFrame,width=30,height=1, fg="blue")
        self.sortie.pack(ipady=0)

        self.entree.insert("1.0","0")
        self.sortie.insert("1.0","0")
        
    
        

        self.descriptionlabel = tk.Label(self.AddTransactionFrame, text="description", fg="blue").pack(expand=True,ipady=0)
        self.description = tk.Text(self.AddTransactionFrame,width=30,height=1, fg="blue")
        self.description.pack(ipady=0)

         #Create a Label
        self.lbdatapicker = tk.Label(self.AddTransactionFrame, text= "Choisir les dates", background= 'gray61', foreground="white").pack(ipady=0)
        #Create a Calendar using DateEntry
        self.cal = DateEntry(self.AddTransactionFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
        self.cal.pack(pady=10)

        self.insertbtn = tk.Button(self.AddTransactionFrame,
                text='Add Transaction', fg="blue",font = "Helvetica 10 bold italic",
                command=self.insertTransaction).pack(expand=True,ipady=0)
        '''Ende widgets def Add transaction'''

        # Add Transaction widgets
        self.labelFilterTransaction = tk.Label(self.FilterTransactionFrame, text="Filter Transaction", fg="blue", font="bold").pack(expand=True,ipady=0)
        self.clientlabelfilter = tk.Label(self.FilterTransactionFrame, text="Client", fg="blue").pack(expand=True,ipady=0)
        values1 = self.dbm.SelectColumn("clientname","./dbs/DBClient.db","Client",None)
        values1.append("ALL")
        self.clientfilter = Combobox(self.FilterTransactionFrame, values= values1)
        self.clientfilter['state'] = 'readonly'
        #self.client = tk.Text(self.FilterTransactionFrame,width=30,height=1, fg="blue")
        self.clientfilter.pack(ipady=0)
       
         #Create a Label
        self.lbdatapickertrans = tk.Label(self.FilterTransactionFrame, text= "Choose a Date", background= 'gray61', foreground="white").pack(ipady=0)
        #Create a Calendar using DateEntry
        self.caltrans = DateEntry(self.FilterTransactionFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
        self.caltrans.pack(pady=10)
        self.caltransend = DateEntry(self.FilterTransactionFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
        self.caltransend.pack(pady=10)

        self.insertbtn = tk.Button(self.FilterTransactionFrame,
                text='Filter Transaction', fg="blue",font = "Helvetica 10 bold italic",
                command=self.filterTransaction).pack(expand=True,ipady=0)
        '''Ende widgets def filter transactions'''
        
       
        
        self.Facturebtn = tk.Button(self,
                text='Create Facture', fg="blue",font = "Helvetica 10 bold italic",
                command=self.Facture).pack(expand=True,ipady=0)
        
        self.text = tk.StringVar()
        self.text.set("Benefice:")
        
        self.labelstatus = tk.Label(self, textvariable= self.text, fg="blue", font="bold").pack(expand=True,ipady=0)
        
        
        # Add DeleteTransaction widgets
        self.labelDeleteTransaction = tk.Label(self.DeleteTransactionFrame, text="Delete Transaction", fg="blue", font="bold").pack(expand=True,ipady=0)
        self.Transactionnamelabeldel = tk.Label(self.DeleteTransactionFrame, text="Name", fg="blue").pack(expand=True,ipady=0)

        values1 = self.dbm.SelectColumn("id",self.db,self.table,None)
        values1.append("ALL")

        self.Transactionnamedel = Combobox(self.DeleteTransactionFrame, values= values1)
        self.Transactionnamedel.pack(pady=0)

        self.Deletebtn = tk.Button(self.DeleteTransactionFrame,
            text='Delete Transaction', fg="blue",font = "Helvetica 10 bold italic",
            command=self.DeleteTransaction).pack(expand=True,ipady=0)
        # Benefice de la transaction
        self.benefice = 0.0
        # transaction table
        self.ViewTransactions()

        

        #self.configure(background='skyblue')
        self.configure(background='MediumAquamarine')

    def Facture(self):
        print("Facture en cours de creation")
        self.printtree()
    
    def Getproductprice(self, varproductname):
        print("")

        

    def clearViewFrame(self):
         for widgets in self.ViewFrame.winfo_children():
            widgets.destroy()


    def insertTransaction(self):

        try:
            db = self.db
            connection1 = sqlite3.connect(db)
            productname = str(self.productname.get()) 
            entreeb = float(self.entree.get("1.0",'end-1c'))
            sortieb = float(self.sortie.get("1.0",'end-1c'))

            #print("I am here just after sortieb")
            #now = datetime.now() # current date and time
            #hour = now.strftime("%H")
            transactionb = str(self.client.get()) #+ str(hour)
            description = str(self.description.get("1.0",'end-1c'))

            #Get prixvente of the product
            dbm = DBManagement("DBproduit","produit","productname",productname,"")
            prixvente = dbm.SelectColumn("prixvente","./dbs/DBProduit.db","produit",productname,"productname")
            prixvente = float(prixvente[0])
            prixachat = dbm.SelectColumn("prixachat","./dbs/DBProduit.db","produit",productname,"productname")
            prixachat = float(prixachat[0])

            #print("I am here before Nombre")

            NombreProduits = dbm.SelectColumn("Nombre","./dbs/DBProduit.db","produit",productname,"productname")
            NombreProduits = NombreProduits[0]

            if(NombreProduits != None):
                NombreProduits = float(NombreProduits)
            else:
                NombreProduits = 0.0


           

            benefice = dbm.SelectColumn("Benefice","./dbs/DBProduit.db","produit",productname,"productname")
            benefice = benefice[0]

            benefice = float(benefice)

            if(benefice != None):
                benefice = float(benefice)
            else:
                benefice = 0.0

           
            print(NombreProduits)

            PlusNombreProduits = float(str(NombreProduits)) + float(entreeb)
            MoinsNombreProduits = float(str(NombreProduits)) - float(sortieb)

            if(self.client.get() == "depot"):
               print("client is depot")
               updated = self.dbm.UpdateColumn("productname","./dbs/DBproduit.db","produit",self.productname.get(),"Nombre",PlusNombreProduits)
               benefice = 0.0
               if(updated):
                   print("Produits updated")
            elif( MoinsNombreProduits < 0):
                # Check avialibility
                print("Quantite of "+productname+" not available")
                return
            else:
                self.dbm.UpdateColumn("productname","./dbs/DBproduit.db","produit",self.productname.get(),"Nombre", MoinsNombreProduits)
                benefice = benefice * sortieb


            prixdelatransaction = (prixvente * sortieb) - (prixachat * entreeb)
            print(prixvente)
            print(prixachat)
            
            
            cursor1 = connection1.cursor()
            cursor1.execute("insert into Transaktionen(id,productname,entress,sorties,description,createdate,Transaktionen,prixtransaction,Benefice) values (?,?,?,?,?,?,?,?,?)",(cursor1.lastrowid, productname,entreeb,sortieb,description,self.cal.get_date(),transactionb,prixdelatransaction,benefice))
            
            connection1.commit()
            messagebox.showinfo(title="Add Transaction", message="Transaction  Sucessful added", icon="info")
        except Exception as e:
            messagebox.showinfo(title="Exception", message=str(e), icon="error")
        finally:
            if connection1:
                connection1.close()
        #update table view after insert        
        for i in self.tree.get_children():
           self.tree.delete(i)
        self.ViewTransactions()


    def filterTransaction(self):
        #self.clearViewFrame()
        for i in self.tree.get_children():
           self.tree.delete(i)

        db = self.db
        #connection1 = sqlite3.connect(db)
        clientnamename = str(self.clientfilter.get()) 
        transdate = self.caltrans.get_date()

        if(clientnamename == "ALL"):
            Totalbenefice = 0.0
            rows = self.dbm.ViewTable()
            for row in rows:
                if(row[8]!= None):
                    Totalbenefice = Totalbenefice + float(row[8])
            self.text.set( "Total Benefice :" + " : " + str(Totalbenefice))
            
            
        else:
            #rows = self.dbm.ViewTable(clientnamename,"Transaktionen",str(transdate),"createdate")
            Totalbenefice = 0.0
            rows = self.dbm.ViewTable(clientnamename,"Transaktionen",str(self.caltrans.get_date()),"createdate",str(self.caltransend.get_date()))
            for row in rows:
                if(row[8]!= None):
                    Totalbenefice = Totalbenefice + float(row[8])
            self.text.set( "Total Benefice :" + " : " + str(Totalbenefice))

        self.Filltreeview(rows)
        
        

    def Filltreeview(self,rows):
        
        #if(not bool(self.tree.winfo_ismapped())):
             # Add a Treeview widget
            
        self.tree.column("# 1", anchor=CENTER)
        self.tree.heading("# 1", text="ID")
        self.tree.column("# 2", anchor=CENTER)
        self.tree.heading("# 2", text="Nom du produit")
        self.tree.column("# 3", anchor=CENTER)
        self.tree.heading("# 3", text="entrees")
        self.tree.column("# 4", anchor=CENTER)
        self.tree.heading("# 4", text="sorties")
        self.tree.column("# 5", anchor=CENTER)
        self.tree.heading("# 5", text="Date de transaction")
        self.tree.column("# 6", anchor=CENTER)
        self.tree.heading("# 6", text="Description")
        self.tree.column("# 8", anchor=CENTER)
        self.tree.heading("# 8", text="Nom du client")
        self.tree.column("# 7", anchor=CENTER)
        self.tree.heading("# 7", text="Prix")
        
        #self.tree.column("# 9", anchor=CENTER)
        #self.tree.heading("# 9", text="Benefice")
       
        # Insert the data in self.treeview widget
        for row in rows:
            self.tree.insert('', 'end', text="1",values=row)
        self.tree.pack()


    ''' View all available transactionen'''
    def ViewTransactions(self):
        Totalbenefice = 0.0
        rows = self.dbm.ViewTable()
        for row in rows:
            if(row[8]!= None):
                Totalbenefice = Totalbenefice + float(row[8])
        self.text.set( "Total Benefice :" + " : " + str(Totalbenefice))
                      
        self.Filltreeview(rows)
        # Create an object of Style widget
        

    def printtree(self):

        PrixTotal = 0.0

        # save FPDF() class into
        # a variable pdf
        pdffile = str(self.clientfilter.get()) + str(self.caltrans.get_date()) + ".pdf"
        table = [[]]
        pdf = FPDF()  
        
        # Add a page
        pdf.add_page()
        
        # set style and size of font
        # that you want in the pdf
        
        pdf.set_font("Arial", 'B', size = 45)
        for child in self.tree.get_children():
            #print(self.tree.item(child)["values"])
            table.append(self.tree.item(child)["values"])
            #if(self.tree.item(child)["values"][6]!= None):
            PrixTotal = PrixTotal + float(self.tree.item(child)["values"][6])
        fig, ax = plt.subplots()

            # hide axes
        fig.patch.set_visible(False)

        texttrans = "OliviaNketch: facture de " + str(self.clientfilter.get()) + " Date: " + str(self.caltrans.get_date()) + " Total: " + str(PrixTotal)
        #adding text inside the plot
        #plt.text(-5, 60, texttrans, fontsize = 22)
        plt.title(texttrans)
        #plt.xlabel(texttrans)

        ax.axis('off')
        #ax.axis('tight')

        font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 70}

        columnslist = ["ID", "productname","Entrees", "Sorties", "createdate", "Description","Transaction","Prix","Benefice"]
        df = pd.DataFrame(table, columns=list(columnslist))

        # drop the last column to hide it from customers.
        #df = df.drop('Benefice', axis==1)
        del df['Benefice']
        #print(df)
        location = "./Factures/"+pdffile
        the_table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
        pp = PdfPages(location)
        #pp = PdfPages("testfacture.pdf")
        pp.savefig(fig)
        pp.close()

        fig.tight_layout()
        plt.rc('font',**font)
        plt.rcParams.update({'font.size': 70,})
        #plt.show()
       
        messagebox.showinfo("Facture","Facture crée")

    def DeleteTransaction(self):
        messagebox.showinfo("info","delete transaction " + str(self.Transactionnamedel.get()))
        dbm1 = DBManagement(self.db,self.table,"id",self.Transactionnamedel.get() ,self.query)
        dbm1.deleteItem()
        for i in self.tree.get_children():
           self.tree.delete(i)
        self.ViewTransactions()
    


