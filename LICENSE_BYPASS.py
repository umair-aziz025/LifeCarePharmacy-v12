#!/usr/bin/env python3
"""
================================================================================
 🔓 LIFECAREPHARMACY12 LICENSE BYPASS TOOL
================================================================================
 Author: Security Research Team
 Target: AbuzarSoftWare LifeCarePharmacy12
 
 This tool bypasses the license validation by:
 1. Modifying SQL Server database entries
 2. Patching registry keys
 3. Providing unlimited access
 
 Similar to Nemrah Ahmed subscription bypass!
================================================================================
"""

import os
import sys
import subprocess
import ctypes
import winreg
import shutil
from datetime import datetime, timedelta
import pyodbc
import sqlite3

# ===============================================================================
# CONFIGURATION
# ===============================================================================

LICENSE_CONFIG = {
    "app_name": "LifeCarePharmacy12",
    "vendor": "AbuzarSoftWare",
    "database_name": "LifeCarePharmacy12",
    
    # License table patterns found in analysis
    "license_patterns": {
        "unregistered": "YLIFECARE12AAUnregistered",
        "registered": "YLIFECARE12AARegistered",
    },
    
    # Registry paths to check/modify
    "registry_paths": [
        r"SOFTWARE\AbuzarSoftWare\LifeCarePharmacy12",
        r"SOFTWARE\WOW6432Node\AbuzarSoftWare\LifeCarePharmacy12",
        r"SOFTWARE\AbuzarSoftWare",
    ],
    
    # Database connection templates
    "connection_strings": [
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=.;DATABASE=LifeCarePharmacy12;Trusted_Connection=yes;TrustServerCertificate=yes;",
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=LifeCarePharmacy12;Trusted_Connection=yes;TrustServerCertificate=yes;",
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=.\\SQLEXPRESS;DATABASE=LifeCarePharmacy12;Trusted_Connection=yes;TrustServerCertificate=yes;",
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=LifeCarePharmacy12;Trusted_Connection=yes;TrustServerCertificate=yes;",
    ],
    
    # Default admin credentials (extracted from analysis)
    "default_users": [
        {"username": "ADMIN", "password": "a"},
        {"username": "ADMIN", "password": "1"},
        {"username": "ADMIN", "password": "0236"},
        {"username": "sa", "password": ""},
        {"username": "sa", "password": "sa"},
    ]
}


# ===============================================================================
# UTILITY FUNCTIONS
# ===============================================================================

def is_admin():
    """Check if running as administrator"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def print_banner():
    """Print tool banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔓 LIFECAREPHARMACY12 LICENSE BYPASS TOOL v1.0                              ║
║  ═══════════════════════════════════════════════════════════════════════════ ║
║  Target: AbuzarSoftWare LifeCarePharmacy12                                   ║
║  Methods: Database Patch | Registry Mod | Binary Patch                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def log(message, level="INFO"):
    """Logging function"""
    symbols = {
        "INFO": "[*]",
        "SUCCESS": "[+]",
        "ERROR": "[-]",
        "WARNING": "[!]",
        "DEBUG": "[D]"
    }
    print(f"{symbols.get(level, '[?]')} {message}")


# ===============================================================================
# DATABASE BYPASS METHODS
# ===============================================================================

class DatabaseBypass:
    """Bypass license via SQL Server database modification"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Try to connect to SQL Server database"""
        for conn_str in LICENSE_CONFIG["connection_strings"]:
            try:
                log(f"Trying: {conn_str[:50]}...")
                self.connection = pyodbc.connect(conn_str, timeout=5)
                self.cursor = self.connection.cursor()
                log("Connected to SQL Server!", "SUCCESS")
                return True
            except Exception as e:
                log(f"Failed: {str(e)[:50]}", "DEBUG")
                continue
        
        log("Could not connect to SQL Server", "ERROR")
        return False
    
    def get_license_status(self):
        """Get current license status"""
        try:
            # Try different table names
            tables_to_try = [
                "ClientInstance",
                "SiteInfo", 
                "CompanyInfo",
                "LicenseInfo",
                "Registration"
            ]
            
            for table in tables_to_try:
                try:
                    self.cursor.execute(f"SELECT * FROM {table}")
                    rows = self.cursor.fetchall()
                    if rows:
                        log(f"Found license data in {table}:", "SUCCESS")
                        for row in rows:
                            print(f"     {row}")
                        return table, rows
                except:
                    continue
            
            log("No license table found", "WARNING")
            return None, None
            
        except Exception as e:
            log(f"Error getting license: {e}", "ERROR")
            return None, None
    
    def bypass_license(self):
        """Apply license bypass to database"""
        try:
            # Method 1: Update ClientInstance
            bypass_queries = [
                # Update ClientInstance to registered
                """
                UPDATE ClientInstance 
                SET Name = REPLACE(Name, 'Unregistered', 'Registered')
                WHERE Name LIKE '%Unregistered%'
                """,
                
                # Set ClientID and InstanceID
                """
                UPDATE ClientInstance 
                SET ClientID = 1, ClientInstanceID = 1
                WHERE ClientID IS NULL OR ClientInstanceID IS NULL
                """,
                
                # Update SiteInfo if exists
                """
                IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'SiteInfo')
                BEGIN
                    UPDATE SiteInfo SET Registered = 'Y', Licensed = 'Y'
                END
                """,
                
                # Update any registration flags
                """
                IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                           WHERE COLUMN_NAME = 'Registered')
                BEGIN
                    EXEC('UPDATE ' + 
                         (SELECT TOP 1 TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                          WHERE COLUMN_NAME = ''Registered'') + 
                         ' SET Registered = ''Y''')
                END
                """,
                
                # Extend trial/expiry dates
                """
                IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                           WHERE COLUMN_NAME IN ('ExpiryDate', 'ExpireDate', 'LicenseExpiry'))
                BEGIN
                    UPDATE ClientInstance SET ExpiryDate = '2099-12-31' 
                    WHERE ExpiryDate IS NOT NULL
                END
                """,
            ]
            
            success_count = 0
            for query in bypass_queries:
                try:
                    self.cursor.execute(query)
                    self.connection.commit()
                    success_count += 1
                except Exception as e:
                    log(f"Query skipped: {str(e)[:40]}", "DEBUG")
            
            log(f"Applied {success_count} bypass modifications", "SUCCESS")
            return success_count > 0
            
        except Exception as e:
            log(f"Database bypass failed: {e}", "ERROR")
            return False
    
    def create_admin_user(self):
        """Create a new admin user with full access"""
        try:
            # Insert new admin user
            query = """
            IF NOT EXISTS (SELECT 1 FROM Users WHERE UserName = 'BYPASS_ADMIN')
            BEGIN
                INSERT INTO Users (UserCode, UserName, Password, FatherName, Address, Phone)
                VALUES (
                    (SELECT ISNULL(MAX(UserCode), 0) + 1 FROM Users),
                    'BYPASS_ADMIN',
                    'bypass123',
                    'License Bypass Tool',
                    'Security Research',
                    '00000000000'
                )
            END
            """
            self.cursor.execute(query)
            self.connection.commit()
            log("Created admin user: BYPASS_ADMIN / bypass123", "SUCCESS")
            return True
        except Exception as e:
            log(f"Could not create admin: {e}", "ERROR")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()


# ===============================================================================
# REGISTRY BYPASS METHODS  
# ===============================================================================

class RegistryBypass:
    """Bypass license via Windows Registry modification"""
    
    def __init__(self):
        self.backup_file = f"registry_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.reg"
    
    def backup_registry(self):
        """Backup relevant registry keys"""
        try:
            for reg_path in LICENSE_CONFIG["registry_paths"]:
                backup_cmd = f'reg export "HKLM\\{reg_path}" "{self.backup_file}" /y 2>nul'
                os.system(backup_cmd)
            log(f"Registry backed up to {self.backup_file}", "SUCCESS")
            return True
        except:
            return False
    
    def find_license_keys(self):
        """Search for license-related registry keys"""
        found_keys = []
        
        search_terms = ["AbuzarSoftWare", "LifeCare", "License", "Registration", "Trial"]
        
        for term in search_terms:
            try:
                # Search in HKLM
                result = subprocess.run(
                    f'reg query "HKLM\\SOFTWARE" /s /f "{term}" 2>nul',
                    capture_output=True, text=True, shell=True
                )
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line.strip() and 'HKEY' in line:
                            found_keys.append(line.strip())
                            
                # Search in HKCU
                result = subprocess.run(
                    f'reg query "HKCU\\SOFTWARE" /s /f "{term}" 2>nul',
                    capture_output=True, text=True, shell=True
                )
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line.strip() and 'HKEY' in line:
                            found_keys.append(line.strip())
                            
            except Exception as e:
                log(f"Registry search error: {e}", "DEBUG")
        
        found_keys = list(set(found_keys))
        if found_keys:
            log(f"Found {len(found_keys)} registry keys:", "SUCCESS")
            for key in found_keys[:10]:
                print(f"     {key}")
        
        return found_keys
    
    def patch_registry(self):
        """Apply license bypass to registry"""
        bypass_values = {
            "Licensed": "1",
            "Registered": "1", 
            "TrialMode": "0",
            "ExpiryDate": "99991231",
            "LicenseKey": "BYPASS-UNLIMITED-2099",
            "LicenseStatus": "ACTIVE",
            "IsRegistered": "TRUE",
            "ActivationStatus": "1",
        }
        
        success_count = 0
        
        for reg_path in LICENSE_CONFIG["registry_paths"]:
            try:
                # Try to open/create the key
                key = winreg.CreateKeyEx(
                    winreg.HKEY_LOCAL_MACHINE,
                    reg_path,
                    0,
                    winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY
                )
                
                for name, value in bypass_values.items():
                    try:
                        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
                        success_count += 1
                    except:
                        pass
                
                winreg.CloseKey(key)
                log(f"Patched: HKLM\\{reg_path}", "SUCCESS")
                
            except Exception as e:
                log(f"Could not patch {reg_path}: {e}", "DEBUG")
        
        # Also try 32-bit registry view
        for reg_path in LICENSE_CONFIG["registry_paths"]:
            try:
                key = winreg.CreateKeyEx(
                    winreg.HKEY_LOCAL_MACHINE,
                    reg_path,
                    0,
                    winreg.KEY_WRITE | winreg.KEY_WOW64_32KEY
                )
                
                for name, value in bypass_values.items():
                    try:
                        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
                        success_count += 1
                    except:
                        pass
                
                winreg.CloseKey(key)
                
            except:
                pass
        
        log(f"Applied {success_count} registry patches", "SUCCESS")
        return success_count > 0


# ===============================================================================
# BINARY PATCH METHODS
# ===============================================================================

class BinaryPatch:
    """Patch executable to bypass license checks"""
    
    def __init__(self, exe_path):
        self.exe_path = exe_path
        self.backup_path = exe_path + ".backup"
    
    def backup(self):
        """Create backup of executable"""
        try:
            if not os.path.exists(self.backup_path):
                shutil.copy2(self.exe_path, self.backup_path)
                log(f"Backup created: {self.backup_path}", "SUCCESS")
            return True
        except Exception as e:
            log(f"Backup failed: {e}", "ERROR")
            return False
    
    def find_license_checks(self):
        """Search for license check patterns in binary"""
        patterns = [
            b"Unregistered",
            b"License",
            b"Trial",
            b"Expire",
            b"Register",
            b"Activation",
            b"YLIFECARE",
        ]
        
        found = []
        try:
            with open(self.exe_path, 'rb') as f:
                data = f.read()
                
            for pattern in patterns:
                offset = 0
                while True:
                    pos = data.find(pattern, offset)
                    if pos == -1:
                        break
                    found.append((pattern.decode('utf-8', errors='ignore'), hex(pos)))
                    offset = pos + len(pattern)
            
            if found:
                log(f"Found {len(found)} license-related strings:", "SUCCESS")
                for pattern, offset in found[:10]:
                    print(f"     {pattern} @ {offset}")
                    
        except Exception as e:
            log(f"Binary analysis error: {e}", "ERROR")
        
        return found
    
    def patch_strings(self):
        """Patch license-related strings in binary"""
        try:
            self.backup()
            
            with open(self.exe_path, 'rb') as f:
                data = bytearray(f.read())
            
            patches = [
                # Replace "Unregistered" with "Registered  " (same length)
                (b"Unregistered", b"Registered  "),
                # Replace trial messages
                (b"Trial Version", b"Full Version "),
                (b"TRIAL VERSION", b"FULL VERSION "),
            ]
            
            patch_count = 0
            for old, new in patches:
                if len(old) == len(new):
                    while old in data:
                        pos = data.find(old)
                        data[pos:pos+len(new)] = new
                        patch_count += 1
            
            if patch_count > 0:
                with open(self.exe_path, 'wb') as f:
                    f.write(data)
                log(f"Applied {patch_count} binary patches", "SUCCESS")
                return True
            else:
                log("No patchable strings found", "WARNING")
                return False
                
        except Exception as e:
            log(f"Binary patch failed: {e}", "ERROR")
            return False
    
    def restore(self):
        """Restore from backup"""
        try:
            if os.path.exists(self.backup_path):
                shutil.copy2(self.backup_path, self.exe_path)
                log("Restored from backup", "SUCCESS")
                return True
        except Exception as e:
            log(f"Restore failed: {e}", "ERROR")
        return False


# ===============================================================================
# MAIN BYPASS ORCHESTRATOR
# ===============================================================================

def run_full_bypass(exe_path=None):
    """Run complete license bypass"""
    print_banner()
    
    if not is_admin():
        log("Not running as Administrator!", "WARNING")
        log("Some features may not work. Right-click and Run as Administrator.", "WARNING")
        print()
    
    results = {
        "database": False,
        "registry": False,
        "binary": False
    }
    
    # Phase 1: Database Bypass
    log("=" * 60)
    log("PHASE 1: DATABASE LICENSE BYPASS")
    log("=" * 60)
    
    db = DatabaseBypass()
    if db.connect():
        table, data = db.get_license_status()
        if db.bypass_license():
            results["database"] = True
        db.create_admin_user()
        db.close()
    else:
        log("Database bypass skipped - no connection", "WARNING")
    
    print()
    
    # Phase 2: Registry Bypass
    log("=" * 60)
    log("PHASE 2: REGISTRY LICENSE BYPASS")
    log("=" * 60)
    
    reg = RegistryBypass()
    reg.backup_registry()
    reg.find_license_keys()
    if reg.patch_registry():
        results["registry"] = True
    
    print()
    
    # Phase 3: Binary Patch (if executable provided)
    if exe_path and os.path.exists(exe_path):
        log("=" * 60)
        log("PHASE 3: BINARY PATCH")
        log("=" * 60)
        
        binary = BinaryPatch(exe_path)
        binary.find_license_checks()
        if binary.patch_strings():
            results["binary"] = True
    
    print()
    
    # Summary
    log("=" * 60)
    log("BYPASS SUMMARY")
    log("=" * 60)
    
    for method, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED/SKIPPED"
        print(f"     {method.upper()}: {status}")
    
    if any(results.values()):
        print()
        log("LICENSE BYPASS APPLIED! 🎉", "SUCCESS")
        log("New admin credentials: BYPASS_ADMIN / bypass123", "SUCCESS")
        log("Restart the application to apply changes.", "INFO")
    else:
        print()
        log("No bypass methods succeeded", "ERROR")
        log("Try running as Administrator or check SQL Server connection", "WARNING")
    
    return results


# ===============================================================================
# CLI INTERFACE
# ===============================================================================

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="LifeCarePharmacy12 License Bypass Tool"
    )
    parser.add_argument(
        "--exe", "-e",
        help="Path to abuzar.exe for binary patching",
        default=None
    )
    parser.add_argument(
        "--database-only", "-d",
        action="store_true",
        help="Only apply database bypass"
    )
    parser.add_argument(
        "--registry-only", "-r", 
        action="store_true",
        help="Only apply registry bypass"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Test mode - show what would be done"
    )
    
    args = parser.parse_args()
    
    if args.database_only:
        print_banner()
        db = DatabaseBypass()
        if db.connect():
            db.get_license_status()
            db.bypass_license()
            db.create_admin_user()
            db.close()
    elif args.registry_only:
        print_banner()
        reg = RegistryBypass()
        reg.find_license_keys()
        reg.patch_registry()
    else:
        run_full_bypass(args.exe)


if __name__ == "__main__":
    main()
