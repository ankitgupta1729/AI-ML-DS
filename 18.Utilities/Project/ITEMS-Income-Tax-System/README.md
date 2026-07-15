# ITEMS — Income Tax Evaluation & Maintenance System

> A complete, modern re-implementation of the **Income Tax Evaluation & Maintenance System**
> specified in `project.pdf` — a workspace for tax practitioners to maintain client
> records, file **original & revised** income-tax returns with automatic tax computation,
> keep firm accounts (**Trading A/c, P&L A/c, Balance Sheet**) and generate statutory reports.

<p align="center">
  <b>🔗 Live demo:</b> <a href="https://ankitgupta1729.github.io/items-income-tax-system/">https://ankitgupta1729.github.io/items-income-tax-system/</a><br>
  <sub>Works on laptop, tablet and mobile · no install required</sub>
</p>

Sign in with **`admin` / `admin@123`** (or **`operator` / `items@2025`**).

---

## 1. What's in this project

This repository ships the system in **two forms**, so it satisfies both the
"Visual Basic + Oracle" brief and the "accessible from any browser via a link" brief:

| Deliverable | Folder | Purpose | Status |
|---|---|---|---|
| **Production application** | [`src/`](src/) | ASP.NET **Web Forms (VB.NET)** + **Oracle** (ODP.NET). The real, deployable system. | Full source + run guide |
| **Live web demo** | [`webapp/`](webapp/) | Self-contained HTML/CSS/JS app with the identical schema, modules and tax engine. Deployed to GitHub Pages. | ✅ Live & tested |
| **Oracle database** | [`database/`](database/) | Schema DDL, seed data, audit triggers, report views. | ✅ |
| **Documentation** | [`docs/`](docs/) | User & feature guide (PDF), screenshots. | ✅ |
| **Demo video** | [`demo-video/`](demo-video/) | Narrated MP4 walkthrough + slide deck + script. | ✅ |

> The web demo and the VB.NET app implement the **same seven modules, the same
> five-table data model and the same tax computation** — the web demo simply stores
> data in the browser (localStorage) so it can run on GitHub Pages with no server.

---

## 2. Modules (mapped to the SRS)

The seven modules from `project.pdf` §5 are all implemented:

1. **Client Information** — add / update / delete clients; PAN is the validated primary key.
2. **Original Return** — file the original return for an assessment year; tax is computed automatically.
3. **Revised Return** — file a correction; the system enforces that an original return already exists.
4. **Trading Account** *(firms)* — debit/credit sides with automatic balancing.
5. **Profit & Loss Account** *(firms)* — full expense/income ledger with balancing.
6. **Balance Sheet** *(firms)* — assets vs. liabilities & capital with balancing.
7. **Report Generation** — the four statutory reports (return history, returns in a fiscal,
   total returns in a fiscal, revised returns by client), printable to PDF.

Security (SRS §7 & §15): forms-based login, SHA-256 password hashes, and Oracle
audit triggers that log every insert/update/delete with user, table and timestamp.

---

## 3. Technology stack

| Layer | Production (`src/`) | Live demo (`webapp/`) |
|---|---|---|
| UI | ASP.NET Web Forms (`.aspx`) | HTML5 + CSS3 (responsive, light/dark) |
| Language | **VB.NET** | Vanilla JavaScript (ES5+) |
| Data access | ODP.NET Managed (`Oracle.ManagedDataAccess`) | localStorage |
| Database | **Oracle** 12c+ / XE / Autonomous DB | in-browser |
| Tax engine | `TaxEngine.vb` | `tax.js` (identical logic) |
| Runtime | .NET Framework 4.8 / IIS | any modern browser |

---

## 4. Run the live demo locally (no build)

```bash
cd webapp
python3 -m http.server 8080
# open http://localhost:8080
```

Everything runs client-side. Use the **🧭 guided tour** (top bar) for a walkthrough,
and **🌓** to toggle light/dark. To reset the sample data, run `ITEMS.reset()` in the
browser console.

---

## 5. Run the production app (VB.NET + Oracle)

### Prerequisites
- Windows with **IIS** / **IIS Express**, **Visual Studio 2019/2022** (or MSBuild)
- **.NET Framework 4.8** developer pack
- An **Oracle** database — local **Oracle XE 21c**, or a free **Oracle Autonomous
  Database (Always Free)** on Oracle Cloud
- NuGet package **Oracle.ManagedDataAccess** (restored automatically)

### Step 1 — Create the database
Run the scripts in [`database/`](database/) **in order**:

```sql
-- as a privileged user (SYSTEM / ADMIN)
@01_create_user.sql        -- creates the ITEMS schema/user

-- then connect as ITEMS and run:
@02_create_schema.sql      -- 5 module tables + APP_USER + AUDIT_LOG
@03_seed_data.sql          -- demo clients, returns, firm accounts, logins
@04_triggers_audit.sql     -- audit triggers + report views
```

### Step 2 — Point the app at your database
Edit the connection string in [`src/ITEMS/Web.config`](src/ITEMS/Web.config):

```xml
<add name="ItemsDb"
     connectionString="User Id=ITEMS;Password=Items#2025;Data Source=localhost:1521/XEPDB1;"
     providerName="Oracle.ManagedDataAccess.Client" />
```

For Autonomous DB, download the wallet, set `TNS_ADMIN` to the wallet folder, and use
the TNS alias (e.g. `Data Source=itemsdb_high`).

### Step 3 — Build & run
```powershell
cd src
nuget restore ITEMS.sln        # or let Visual Studio restore
msbuild ITEMS.sln /p:Configuration=Debug
# Press F5 in Visual Studio, or host the site in IIS.
```

Browse to the site and sign in with `admin / admin@123`.

---

## 6. Directory structure

```
ITEMS-Income-Tax-System/
├── README.md                     ← you are here
├── webapp/                       ← live web demo (deployed to GitHub Pages)
│   ├── index.html
│   ├── css/styles.css
│   └── js/  (tax.js · db.js · app.js)
├── src/                          ← production ASP.NET Web Forms (VB.NET)
│   ├── ITEMS.sln
│   └── ITEMS/
│       ├── Web.config
│       ├── Site.Master(.vb)
│       ├── Login / Default / Clients / ClientEdit
│       ├── Returns / ReturnEdit / FirmAccount / Reports  (.aspx + .vb)
│       └── App_Code/  (OracleDb · Models · TaxEngine · Security · *Repository)
├── database/                     ← Oracle SQL scripts (run 01→04)
├── docs/                         ← PDF user guide + screenshots
└── demo-video/                   ← narrated MP4 + slides + script
```

---

## 7. Tax computation

Old-regime slabs (AY 2024-25) for individuals; flat 30% for firms:

| Total income | Rate |
|---|---|
| up to ₹2,50,000 | 0% |
| ₹2,50,001 – ₹5,00,000 | 5% |
| ₹5,00,001 – ₹10,00,000 | 20% |
| above ₹10,00,000 | 30% |

Then: rebate u/s 87A (income ≤ ₹5,00,000), surcharge (10/15/25/37% by income band),
4% health & education cess, less TDS / advance / self-assessment tax → **balance
payable or refund**. The same logic lives in `tax.js` and `TaxEngine.vb`.

> ⚠️ Figures are illustrative for demonstration and training; verify against the
> current Finance Act before any real filing.

---

## 8. Demo credentials

| User | Password | Role |
|---|---|---|
| `admin` | `admin@123` | Administrator |
| `operator` | `items@2025` | Operator |

---

## 9. Credits

Re-engineered from the *Income Tax Evaluation & Maintenance System* project report
(`18.Utilities/Project/project.pdf`). Original concept: VC++ 6.0 + Oracle 8i;
this edition modernises it to VB.NET + Oracle with a browser-accessible demo.
