# 🔒 LIFECAREPHARMACY12 - COMPLETE SECURITY AUDIT REPORT
## AbuzarSoftWare PowerBuilder Pharmacy Management System

**Audit Date:** 2025-03-04  
**Target:** LifeCarePharmacy12 (E:\2019-Jan-16.rar backup)  
**Auditor:** Security Research Team  

---

## 📋 EXECUTIVE SUMMARY

This audit reveals **CRITICAL SECURITY VULNERABILITIES** in the LifeCarePharmacy12 by AbuzarSoftWare:

| Category | Risk Level | Findings |
|----------|------------|----------|
| **User Credentials** | 🔴 CRITICAL | **17+ plaintext passwords** extracted from SQL backup |
| **License Bypass** | 🔴 CRITICAL | License stored in ClientInstance table, easily bypassed |
| **Password Protection** | 🟡 MEDIUM | RAR3 encryption on sqldata.rat (crackable via GPU) |
| **SQL Injection** | 🟡 MEDIUM | Dynamic SQL in stored procedures |
| **Hardcoded Secrets** | 🟡 MEDIUM | WebSMS credentials stored in Preferences |

---

## 🔑 CREDENTIAL EXTRACTION

### Database User Credentials (From SQL Backup)

| UserCode | Username | Password | Notes |
|----------|----------|----------|-------|
| - | **TASLEEM** | `786` | AL-LATIF Company |
| - | **MAQSOOD** | `786` | AL-LATIF Company |
| - | **MEHRABAN** | `786` | ISB Location |
| - | **TOUSEE** | `786` | RWP Location (03418067537) |
| - | **JANJUA** | `1122` | JAWAD ALI (03275160377) |
| - | **ADMIN** | `a` / `1` / `0236` | Multiple admin accounts |
| - | **RAB NAWAZ** | `7890` | - |
| - | **SUBHAN** | `5550` | - |
| - | **RIZWAN** | `123` | - |
| - | **DILAWAR** | `1230` | - |
| - | **NASIR** | `3` | BALAH MIRPUR AK (0315394030) |
| - | **MASROOR** | `25` | (0341-8122106) |
| - | **JAMEEL** | `25` | - |
| - | **TEST** | `1` / `2` | Test accounts |
| - | **SALESMAN** | `1` | (ABC1234567) |
| - | **ABC** | `ABC1234567` | Test account |
| - | **PURCHASE** | `1` | - |

### Table Schema Discovered
```sql
Users (
    UserCode SMALLINT PRIMARY KEY,
    UserName NVARCHAR(255),
    Password NVARCHAR(255),  -- PLAINTEXT!
    FatherName NVARCHAR(255),
    Address NVARCHAR(255),
    Phone VARCHAR(20)
)
```

**⚠️ VULNERABILITY:** Passwords stored in PLAINTEXT - no hashing!

---

## 🔓 LICENSE BYPASS MECHANISM

### License Storage Pattern
The license is stored in the `ClientInstance` table:

```
Format: Y<CLIENTNAME>AA<STATUS>
Examples found:
- YLIFECARE12AAUnregistered  (Current instance - NOT REGISTERED)
- YSHAHZADIBMAAUnregistered  (Another client)
```

### License Bypass Method

**Option 1: Database Modification**
```sql
-- Change registration status
UPDATE ClientInstance 
SET Name = 'LIFECARE12', 
    ClientID = 1, 
    ClientInstanceID = 1
WHERE Name LIKE '%Unregistered%';

-- Or modify the registration flag directly
UPDATE SiteInfo SET Registered = 'Y' WHERE Registered = 'N';
```

**Option 2: Registry Modification**
The software likely checks Windows Registry for:
- `HKLM\SOFTWARE\AbuzarSoftWare\LifeCarePharmacy12`
- License key validation

**Option 3: Binary Patching**
PowerBuilder apps typically have license checks in:
- Main EXE event handlers (Open, Activate)
- PBD library initialization functions

Look for conditional jumps (JE/JNE) after license validation calls.

---

## 🗄️ DATABASE ANALYSIS

### SQL Server Configuration
- **Database:** LifeCarePharmacy12
- **Server:** Local SQL Server Express (likely)
- **Authentication:** SQL Server Auth (sa account probable)

### Key Tables Identified
| Table | Purpose | Sensitive Data |
|-------|---------|----------------|
| `Users` | User accounts | Plaintext passwords |
| `Accounts` | Customer/Supplier data | Financial info |
| `SaleLedger` | Sales transactions | Revenue data |
| `PurLedger` | Purchase records | Cost data |
| `ItemInventory` | Stock levels | Inventory values |
| `ClientInstance` | License info | Registration status |
| `Preferences` | App config | WebSMS credentials |

### Sensitive Stored Procedures
```sql
SP_SetUserResponsibility  -- Role management
SP_ValidateSaleInvoice    -- Transaction validation
SP_GenerateReceipt        -- Financial operations
SP_CRS_GetClientInstanceInfo -- License checking
```

---

## 📁 ENCRYPTED ARCHIVE ANALYSIS

### sqldata.rat (Password Protected RAR)
- **Size:** 7.69 MB
- **Encryption:** RAR3-hp (hashcat mode 12500)
- **Contents:** SQL Server system databases
  - master.mdf, mastlog.ldf
  - msdbdata.mdf, msdblog.ldf
  - pubs.mdf, northwnd.mdf
  - distmdl.mdf, distmdl.ldf

### Hash for GPU Cracking
```
$RAR3$*1*4316055ad35fee85*ce0bb9ae*16512*524288*1*65f33795bf8f24d6fb9d66adad50c503804f8e6dd6df7e328def6a7664794d955b6645ee130462a0afef67448ed3346b59164e493a7f509b06303aa8f0dc46909f7f5a0e96ddecc37cf58acebd6584bbdab44b8ea86cb25828c643bca37361a81e96c1034d7bd91cc76a29443d065f9ef7b2938b4f651707e0bdaa416ea982a998eb6319150adaaa91b0254d223c16114f93107effeb12ee6f744703edb38336bd79fdb98072d137b6b56342a1c418d999954d56be37f5c67a0fc98edce879e3f26046afab8f83a33731cf6a35cfb2a4f5a7c51acc86a607e41df8b595374eb3726b9efff4396c06261fdb02880ecaa447fb48baac705ed26e998a15d113c52d7b51cf9be0ea1faed249a9589b429ab09afc3e3c605fe3c13eee8d759f0b8977cd1f95b5e689514f50ec2860310bd704ae93626c938f918a7a00e3c276c2b2eb9df96e67864b32c6905f322477e2328089e92bc9e9f8206a795bc606dc2ab9f74121315c0230a20de2ccef6f23a712c0335d522874cd9d1dbb0bdf0094d4cecf08047376e05bf5b858eb39f94fb7cab166c1458c89d05f50354765288e289ab2656964e41058c04a1382918236fc20db8e01cc6226fbd827e4f08a75ffe89188f1c01fbedae791cce5bc9b5b2f5430f99e325cf4701b9763b8fbb3f4185f5dd856e9c940b3a7f489a8e6e3e49591c8867f0aaf41497b60817abd92368f8597c54a3d7822dfc8cea85c569fde8ea8239d3b437af9fcf09e16388ed70b6e2feca1619ea699d3ec03402842ad8519b77ef4ab9198f7439259208c3bdb533cd7ece758c3990c2ba9a824490cc2db304fc384c95fe18b5f8aa253b9624fd2dcc56087de419f0b964fa877c44701e32f64a29ad9bd48620d11c3beafe8c0ff0ea04a12c3220a479f016d36c6491cec92923ec5deb8fa8a8ffbb139c6bef644b5c57a07f9a8d56efb146149d1a3c600bb30517122c238a65006cdcb42261b0781df9c02934f189b95fe4ef4f12997c81249616ff75395a7ae92a436bcbbaeec3fa9266f5b9fec9bc7a217e914a40cce37f705d20549f760ccec915f857332859ee512efa126d125b81a7847d37972f7b531f2b8be778992daa67ef32ef1a4804f4d4421b2048397d9a0e2975e301324b5d50720cc3300b6511ddb002fde5f5e55baf4a0426c732d25fcd675f3df597600935f6b7f0df35d11cd71e20f2ecfe7461b6f5f943477019d638ad137b281efbd4cdc2f75319313d54df60530256fcf30ee780acd8074c0613a9a49c957ae71be089b5868af92849cb4aaac318c41c4bf7dd32e6f3ed2a5462434d0e36969c8732942110b5c020ffa193670d32c54027250d3fb55efdc31643a94d33bac107af929f71322d2cb1a194fbb9bb7a3bc8cc1962fc0a46eea1a70c60dddc95c0da46ba3a2144db615b0c3798f6abef862e166eba3b545e76f8beb467d581f303e22ce21a3a44959cacac68f61ce2c913728ec6a001df2d9ad9e8ee6c34b4f89db3cc430b661648694e915731938eb3f76d78c5d7441a3b8ae7260e9f2acfb20d113c004c831d7a2cfda276b3d4552dfbe646e27f11a75185a04c911f61c4966a3cd6002ef7890425a4740ecdf0cfa3146fde92c6773b8c4da858d53e8d86790c9f289bb936b20c2e44feefc1256d0153d0fc7772bb51b2560ee7d9e2083d3cc8da6a8c71177149d90ddaf75d91f56cbd1c88c63431c7724f22ab9b0ad45093cb5c62dacbfac21cd999557b6a2d2e3500ff92113b63799910af4c6c3a0ced33dd00a596b252da8532b836e4ce9ed11e5b4196c6acb4de27cf8b217524bbb4a2b24fa6af48066a8f5b253202626fec7e78cb40abb56ff12e4daa9b5ddf730c35abf7831e72753571f594f9d43a88350418fe9a29a6f31e9da22ebf8e9f093e0558cc3a172b7217ffd5b8e4a65a64f8d2690b4c3b5d7b98f7f0d54a1b8941a51905ded64620900917ccf161080d8d2319987382615ab8708d2e4710c1835f1f03b9a1f5a6fcb985c73fdd5ee964a27826a3d11c63b548d58e6cb652638e17529b280184aa474557555d78ac16777169194f949*33:1::Data\\distmdl.ldf
```

### Cracking Command (Google Colab GPU)
```bash
hashcat -m 12500 -a 0 hash.txt rockyou.txt --force -O
hashcat -m 12500 -a 3 hash.txt ?a?a?a?a?a --increment --force -O
```

---

## 🌐 EXTERNAL SERVICES CONFIGURATION

### WebSMS Integration (Found in Preferences)
```
WEBSMSUserID: <configured in database>
WEBSMSPassword: <configured in database>
WEBSMSMask: <configured in database>
```

**⚠️ VULNERABILITY:** SMS gateway credentials stored in database!

---

## 🔧 TECHNICAL DETAILS

### Application Stack
| Component | Technology |
|-----------|------------|
| Frontend | PowerBuilder 12.5 |
| Database | Microsoft SQL Server |
| Backup DB | MS Access (Script.mdb) |
| Reports | DataWindow technology |
| Barcode | Custom PBD libraries |
| Web Services | SOAP (EasySoap125.dll) |

### File Structure
```
AbuzarSoftWare/
├── Application/
│   ├── abuzar.exe (1.1MB) - Main executable
│   ├── *.pbd (PowerBuilder libraries)
│   ├── *.dll (Runtime libraries)
│   └── Script.mdb (Scripts database)
├── Data/
│   ├── sqldata.rat (ENCRYPTED - SQL DBs)
│   └── extracted_sqldata/ (FAILED extraction)
├── BackUp/
│   ├── LifeCarePharmacy12dbdump.bak (161MB)
│   └── old LifeCarePharmacy12DBDump.BAK (1.6GB)
└── AutoBackUp/
    └── Auto*.BAK files
```

---

## 💡 EXPLOITATION SUMMARY

### 1. Immediate Access (No Cracking Required)
- Use extracted credentials to login
- Default admin accounts available: ADMIN/a, ADMIN/1, ADMIN/0236

### 2. License Bypass
- Modify ClientInstance table in database
- Change "Unregistered" status
- Binary patch the license check in PBD files

### 3. Full Database Access
- The unencrypted .BAK files contain ALL business data
- Can restore to local SQL Server for full access
- Contains: customers, suppliers, transactions, inventory

### 4. Encrypted Archive
- Use Google Colab GPU cracker (provided notebook)
- hashcat mode 12500 with rockyou.txt
- Try Pakistani common passwords first

---

## 📱 CONTACT INFORMATION FOUND

| Name | Phone | Role |
|------|-------|------|
| JAWAD ALI (JANJUA) | 03275160377 | User |
| TAHIR | 0346-5419261 | User |
| TOUSEE | 03418067537 | User |
| MASROOR | 0341-8122106 | User |
| NASIR | 0315394030 | User |
| MEHRABAN | 0336-1598225 | User |

---

## 🛡️ RECOMMENDATIONS

### For Security Researchers
1. **Credential Testing:** Use extracted passwords on admin accounts
2. **License Bypass:** Modify database ClientInstance table
3. **RAR Cracking:** Use provided Colab notebook with GPU
4. **Binary Analysis:** Use Ghidra for PBD/EXE reverse engineering

### For Vendor (AbuzarSoftWare)
1. **Hash all passwords** using bcrypt/PBKDF2
2. **Implement license obfuscation** with hardware binding
3. **Encrypt database backups** 
4. **Remove hardcoded credentials** from database
5. **Use parameterized queries** to prevent SQL injection

---

**Report Generated:** 2025-03-04  
**Classification:** CONFIDENTIAL - FOR AUTHORIZED RESEARCH ONLY
