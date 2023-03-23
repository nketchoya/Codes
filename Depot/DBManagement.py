import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import messagebox


# import time

class DBManagement:
    def __init__(self, db, table, rowname, rowvalue,query):
      self.db = db
      self.table = table
      self.rowname = rowname
      self.rowvalue = rowvalue
      self.query = query

      # Check if table exists..if not then create

      

         #return rows
    def deleteItem(self):
        """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:
        """
        try:
            yesorno = messagebox.askquestion("Delete Item","Do you really want to delete Item " + self.rowvalue)
            if(yesorno == "yes"):
                conn = sqlite3.connect(self.db)
                sql = "DELETE FROM " + self.table + " Where " + self.rowname + "=?"
                cur = conn.cursor()
                cur.execute(sql, (self.rowvalue,))
                conn.commit()
                return True
            return False
        except Exception as e:
            messagebox.showinfo(title="Exception", message=str(e), icon="error")
    

    # Function .. view table
    def ViewTable(self,filter=None,filterName=None,filter1=None,filterName1=None,Enddate=None):

        
        if(filter == None):
            
            sql_query1 = "select * from " + self.table
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            cur.execute(sql_query1)

            rows = cur.fetchall()

            # Test purpose
            #print(sql_query1)
            #print(rows)
        elif(Enddate!=None):
            sql_query1 = "select * from " + self.table + " where " + filterName + "= '" + filter +"'" + " AND " + filterName1 + ">= '" + filter1 +"' AND " + filterName1 + "<= '" + Enddate +"'"
            #print(sql_query1)
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            cur.execute(sql_query1)
            rows = cur.fetchall()
            #rows = None
        else:
            sql_query1 = "select * from " + self.table + " where " + filterName + "= '" + filter +"'" + " AND " + filterName1 + "= '" + filter1 +"'"
            #print(sql_query1)
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            cur.execute(sql_query1)
            rows = cur.fetchall()
            #rows = None
        return rows

    def CreateTable(self): 
        if(not self.Checkiftableexists()):
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            cur.execute(self.query)


    def Checkiftableexists(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        #get the count of tables with the name
        sqlquery = '''SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?'''
        c.execute(sqlquery,(self.table,))
        #c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='produit' ''')
       # c.execute(sqlquery)

        #if the count is 1, then table exists
        return (c.fetchone()[0]==1) 
	
    def SelectColumn(self,columname,dbvar,tablevar,filter,filterName=None):
        
        # Add Deleteproduct widgets
        if(filter == None):
            sql_query1 = "select " + columname + " from " + tablevar #self.table
            db = dbvar #self.db
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(sql_query1)
            return cur.fetchall()
        else:
            sql_query1 = "select " + columname + " from " + tablevar + " where " + filterName + "= '" + filter +"'"
            #print(sql_query1)
            db = dbvar #self.db
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(sql_query1)
            return cur.fetchone()
          

    def UpdateColumn(self,columnid,dbvar,tablevar,columnidvalue,columname,columnvalue):
        try:
            # Add Deleteproduct widgets
            #print("update function...")
            conn = sqlite3.connect(dbvar)
            cur = conn.cursor()
            sqlquery2 = "UPDATE " + str(tablevar) + " SET "+ columname + " = '" + str(columnvalue) + "' Where " +columnid + " = '" + columnidvalue + "'"
            print(sqlquery2)
            cur.execute(sqlquery2)
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            messagebox.showinfo(title="Exception", message=str(e), icon="error")
            return False

       #finally:
        #   conn.commit()
         #  conn.close()  
        
        
        
        


 
    
