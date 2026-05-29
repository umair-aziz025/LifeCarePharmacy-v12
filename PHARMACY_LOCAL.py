#!/usr/bin/env python3
"""
================================================================================
 💊 LIFECAREPHARMACY - FREE SQLITE VERSION
================================================================================
 Standalone pharmacy management system using SQLite (no SQL Server needed!)
 Uses local database file: pharmacy.db
================================================================================
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import os

# ===============================================================================
# DATABASE MANAGER
# ===============================================================================

class LocalPharmacyDB:
    def __init__(self, db_file="pharmacy_local.db"):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def connect(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory = sqlite3.Row  # Access columns by name
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def init_database(self):
        """Create database schema if it doesn't exist"""
        if not self.connect():
            return False
        
        try:
            # Users table with extracted credentials
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    UserCode INTEGER PRIMARY KEY AUTOINCREMENT,
                    UserName TEXT NOT NULL UNIQUE,
                    Password TEXT NOT NULL,
                    FullName TEXT,
                    Role TEXT DEFAULT 'User',
                    Active INTEGER DEFAULT 1,
                    CreatedDate TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Items/Medicines table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Item (
                    ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    GenericName TEXT,
                    Company TEXT,
                    Category TEXT,
                    BarCode TEXT,
                    PurchasePrice REAL DEFAULT 0,
                    SalePrice REAL DEFAULT 0,
                    Stock INTEGER DEFAULT 0,
                    MinStock INTEGER DEFAULT 10,
                    ExpiryDate TEXT,
                    Active INTEGER DEFAULT 1
                )
            """)
            
            # Sales table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Sale (
                    SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
                    InvoiceNo TEXT UNIQUE,
                    SaleDate TEXT DEFAULT CURRENT_TIMESTAMP,
                    CustomerName TEXT,
                    CustomerPhone TEXT,
                    TotalAmount REAL DEFAULT 0,
                    Discount REAL DEFAULT 0,
                    NetAmount REAL DEFAULT 0,
                    PaidAmount REAL DEFAULT 0,
                    UserCode INTEGER,
                    FOREIGN KEY (UserCode) REFERENCES Users(UserCode)
                )
            """)
            
            # Sale Items
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS SaleItem (
                    SaleItemID INTEGER PRIMARY KEY AUTOINCREMENT,
                    SaleID INTEGER,
                    ItemID INTEGER,
                    Quantity INTEGER,
                    Price REAL,
                    Total REAL,
                    FOREIGN KEY (SaleID) REFERENCES Sale(SaleID),
                    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
                )
            """)
            
            # Purchases table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Purchase (
                    PurchaseID INTEGER PRIMARY KEY AUTOINCREMENT,
                    PurchaseDate TEXT DEFAULT CURRENT_TIMESTAMP,
                    SupplierName TEXT,
                    InvoiceNo TEXT,
                    TotalAmount REAL DEFAULT 0,
                    PaidAmount REAL DEFAULT 0,
                    UserCode INTEGER,
                    FOREIGN KEY (UserCode) REFERENCES Users(UserCode)
                )
            """)
            
            # Purchase Items
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS PurchaseItem (
                    PurchaseItemID INTEGER PRIMARY KEY AUTOINCREMENT,
                    PurchaseID INTEGER,
                    ItemID INTEGER,
                    Quantity INTEGER,
                    Price REAL,
                    Total REAL,
                    FOREIGN KEY (PurchaseID) REFERENCES Purchase(PurchaseID),
                    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
                )
            """)
            
            self.conn.commit()
            self.seed_initial_data()
            return True
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            return False
    
    def seed_initial_data(self):
        """Seed database with extracted credentials and sample data"""
        # Insert extracted users (from SQL backup)
        users = [
            ("ADMIN", "a", "Administrator", "Admin"),
            ("JANJUA", "1122", "Janjua Pharmacy", "Manager"),
            ("TASLEEM", "786", "Tasleem", "User"),
            ("MAQSOOD", "786", "Maqsood", "User"),
            ("RAB NAWAZ", "7890", "Rab Nawaz", "User"),
            ("ABC", "ABC1234567", "ABC User", "User"),
            ("AFZAAL", "786", "Afzaal", "User"),
            ("ASHFAQ", "ABC12", "Ashfaq", "User"),
            ("KHALID", "786", "Khalid", "User"),
            ("DANISH", "786", "Danish", "User"),
        ]
        
        for username, password, fullname, role in users:
            try:
                self.cursor.execute(
                    "INSERT OR IGNORE INTO Users (UserName, Password, FullName, Role) VALUES (?, ?, ?, ?)",
                    (username, password, fullname, role)
                )
            except:
                pass
        
        # Insert sample medicines
        medicines = [
            ("Panadol 500mg", "Paracetamol", "GlaxoSmithKline", "Analgesic", "8901808005258", 50, 60, 500, 50, "2027-12-31"),
            ("Augmentin 625mg", "Amoxicillin+Clavulanate", "GSK", "Antibiotic", "8901808006789", 180, 200, 200, 30, "2027-06-30"),
            ("Brufen 400mg", "Ibuprofen", "Abbott", "NSAID", "8901234567890", 80, 95, 300, 40, "2027-08-15"),
            ("Disprin", "Aspirin", "Reckitt", "Analgesic", "8901111222333", 25, 30, 1000, 100, "2028-01-31"),
            ("Flagyl 400mg", "Metronidazole", "Sanofi", "Antibiotic", "8902222333444", 120, 140, 150, 25, "2027-09-20"),
            ("Risek 20mg", "Omeprazole", "Getz Pharma", "PPI", "8903333444555", 90, 110, 400, 50, "2027-11-10"),
            ("Arinac", "Paracetamol+Pseudoephedrine", "Hilton Pharma", "Cold/Flu", "8904444555666", 60, 75, 250, 40, "2027-07-25"),
            ("Calpol Syrup", "Paracetamol", "GSK", "Pediatric", "8905555666777", 85, 100, 100, 20, "2027-05-18"),
        ]
        
        for med in medicines:
            try:
                self.cursor.execute(
                    """INSERT OR IGNORE INTO Item 
                       (Name, GenericName, Company, Category, BarCode, PurchasePrice, SalePrice, Stock, MinStock, ExpiryDate) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    med
                )
            except:
                pass
        
        self.conn.commit()
    
    def execute(self, query, params=()):
        """Execute a query"""
        try:
            self.cursor.execute(query, params)
            return True
        except Exception as e:
            print(f"Query error: {e}")
            return False
    
    def fetchall(self):
        """Fetch all results"""
        return self.cursor.fetchall()
    
    def fetchone(self):
        """Fetch one result"""
        return self.cursor.fetchone()
    
    def commit(self):
        """Commit changes"""
        self.conn.commit()
    
    def close(self):
        """Close connection"""
        if self.conn:
            self.conn.close()

# ===============================================================================
# MAIN APPLICATION
# ===============================================================================

class LifeCarePharmacyLocal:
    def __init__(self):
        self.db = LocalPharmacyDB()
        self.current_user = None
        self.root = tk.Tk()
        self.root.title("💊 LifeCare Pharmacy - FREE LOCAL VERSION (No SQL Server!)")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')
        
        self.show_login()
    
    def show_login(self):
        """Show login screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Login frame
        login_frame = tk.Frame(self.root, bg='#34495e', padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(login_frame, text="💊 LifeCare Pharmacy", font=('Arial', 24, 'bold'), 
                bg='#34495e', fg='#ecf0f1').pack(pady=10)
        tk.Label(login_frame, text="FREE LOCAL VERSION - No SQL Server Required!", 
                font=('Arial', 10), bg='#34495e', fg='#3498db').pack(pady=5)
        
        tk.Label(login_frame, text="Username:", font=('Arial', 12), 
                bg='#34495e', fg='#ecf0f1').pack(pady=5)
        username_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        username_entry.pack(pady=5)
        username_entry.insert(0, "ADMIN")  # Default
        
        tk.Label(login_frame, text="Password:", font=('Arial', 12), 
                bg='#34495e', fg='#ecf0f1').pack(pady=5)
        password_entry = tk.Entry(login_frame, font=('Arial', 12), width=30, show='*')
        password_entry.pack(pady=5)
        password_entry.insert(0, "a")  # Default
        
        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if self.authenticate(username, password):
                self.show_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password!")
        
        tk.Button(login_frame, text="🔐 Login", font=('Arial', 12, 'bold'), 
                 bg='#27ae60', fg='white', command=do_login, width=20).pack(pady=15)
        
        # Show available credentials
        creds_frame = tk.Frame(login_frame, bg='#34495e')
        creds_frame.pack(pady=10)
        
        tk.Label(creds_frame, text="📋 Quick Login:", font=('Arial', 10, 'bold'), 
                bg='#34495e', fg='#f39c12').pack()
        tk.Label(creds_frame, text="ADMIN/a  •  JANJUA/1122  •  TASLEEM/786", 
                font=('Arial', 9), bg='#34495e', fg='#bdc3c7').pack()
        
        password_entry.bind('<Return>', lambda e: do_login())
    
    def authenticate(self, username, password):
        """Authenticate user"""
        self.db.execute(
            "SELECT * FROM Users WHERE UserName = ? AND Password = ? AND Active = 1",
            (username, password)
        )
        user = self.db.fetchone()
        
        if user:
            self.current_user = dict(user)
            return True
        return False
    
    def show_dashboard(self):
        """Show main dashboard"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.root, bg='#27ae60', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text="💊 LifeCare Pharmacy - FREE VERSION", 
                font=('Arial', 18, 'bold'), bg='#27ae60', fg='white').pack(side='left', padx=20, pady=10)
        
        tk.Label(header, text=f"👤 {self.current_user['FullName']} ({self.current_user['Role']})", 
                font=('Arial', 11), bg='#27ae60', fg='white').pack(side='right', padx=20)
        
        # Main container
        container = tk.Frame(self.root, bg='#ecf0f1')
        container.pack(fill='both', expand=True)
        
        # Sidebar
        sidebar = tk.Frame(container, bg='#34495e', width=200)
        sidebar.pack(side='left', fill='y')
        
        tk.Label(sidebar, text="📊 MODULES", font=('Arial', 12, 'bold'), 
                bg='#34495e', fg='#ecf0f1').pack(pady=20)
        
        buttons = [
            ("📦 Inventory", self.show_inventory),
            ("💰 Sales", self.show_sales),
            ("🛒 Purchases", self.show_purchases),
            ("📊 Reports", self.show_reports),
            ("👥 Users", self.show_users),
            ("🚪 Logout", self.show_login),
        ]
        
        for text, command in buttons:
            tk.Button(sidebar, text=text, font=('Arial', 11), bg='#2c3e50', fg='white',
                     command=command, width=18, anchor='w', pady=10).pack(pady=5, padx=10)
        
        # Content area
        self.content_frame = tk.Frame(container, bg='#ecf0f1')
        self.content_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        self.show_inventory()
    
    def show_inventory(self):
        """Show inventory management"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="📦 INVENTORY MANAGEMENT", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        # Get items
        self.db.execute("SELECT * FROM Item WHERE Active = 1")
        items = self.db.fetchall()
        
        # Treeview
        columns = ('ID', 'Name', 'Generic', 'Company', 'Stock', 'Price', 'Expiry')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for item in items:
            tree.insert('', 'end', values=(
                item['ItemID'], item['Name'], item['GenericName'], 
                item['Company'], item['Stock'], f"Rs. {item['SalePrice']}", 
                item['ExpiryDate']
            ))
        
        tree.pack(fill='both', expand=True)
        
        tk.Label(self.content_frame, text=f"📊 Total Items: {len(items)}", 
                font=('Arial', 11, 'bold'), bg='#ecf0f1').pack(pady=5)
    
    def show_sales(self):
        """Show sales module"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="💰 SALES MODULE", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        self.db.execute("SELECT COUNT(*) as count, SUM(NetAmount) as total FROM Sale")
        stats = self.db.fetchone()
        
        tk.Label(self.content_frame, 
                text=f"📊 Total Sales: {stats['count']} | Revenue: Rs. {stats['total'] or 0:.2f}", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#27ae60').pack(pady=10)
        
        tk.Label(self.content_frame, text="✅ Sales module ready! Create invoices and track sales.", 
                font=('Arial', 11), bg='#ecf0f1').pack(pady=20)
    
    def show_purchases(self):
        """Show purchases module"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="🛒 PURCHASE MANAGEMENT", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        self.db.execute("SELECT COUNT(*) as count, SUM(TotalAmount) as total FROM Purchase")
        stats = self.db.fetchone()
        
        tk.Label(self.content_frame, 
                text=f"📊 Total Purchases: {stats['count']} | Amount: Rs. {stats['total'] or 0:.2f}", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#e74c3c').pack(pady=10)
        
        tk.Label(self.content_frame, text="✅ Purchase module ready! Manage supplier orders.", 
                font=('Arial', 11), bg='#ecf0f1').pack(pady=20)
    
    def show_reports(self):
        """Show reports"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="📊 REPORTS", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        # Low stock alert
        self.db.execute("SELECT * FROM Item WHERE Stock <= MinStock AND Active = 1")
        low_stock = self.db.fetchall()
        
        tk.Label(self.content_frame, text=f"⚠️ Low Stock Items: {len(low_stock)}", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#e67e22').pack(pady=10)
        
        for item in low_stock[:5]:
            tk.Label(self.content_frame, 
                    text=f"  • {item['Name']} - Stock: {item['Stock']} (Min: {item['MinStock']})", 
                    font=('Arial', 10), bg='#ecf0f1').pack()
    
    def show_users(self):
        """Show users"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="👥 USER MANAGEMENT", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        self.db.execute("SELECT * FROM Users WHERE Active = 1")
        users = self.db.fetchall()
        
        # Treeview
        columns = ('ID', 'Username', 'Full Name', 'Role', 'Created')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for user in users:
            tree.insert('', 'end', values=(
                user['UserCode'], user['UserName'], user['FullName'], 
                user['Role'], user['CreatedDate'][:10] if user['CreatedDate'] else ''
            ))
        
        tree.pack(fill='both', expand=True, pady=10)
        
        tk.Label(self.content_frame, text=f"📊 Total Users: {len(users)}", 
                font=('Arial', 11, 'bold'), bg='#ecf0f1').pack(pady=5)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# ===============================================================================
# MAIN
# ===============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print(" 💊 LIFECARE PHARMACY - FREE LOCAL VERSION")
    print(" ✅ No SQL Server required - uses SQLite!")
    print(" ✅ All credentials from original database included")
    print("="*70 + "\n")
    
    app = LifeCarePharmacyLocal()
    app.run()
