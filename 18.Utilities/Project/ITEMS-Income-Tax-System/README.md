# Income Tax Evaluation System

> A modern implementation of the **Income Tax Evaluation & Maintenance System** specified in
> `project.pdf` — a workspace for tax practitioners to maintain client records, file
> **original & revised** income-tax returns with automatic tax computation, keep firm accounts
> (**Trading A/c, P&L A/c, Balance Sheet**) and generate statutory reports.

**Demo sign-in:** `admin` / `admin@123` · `operator` / `demo@2025`

---

## 1. What's in this project

The system ships in **two editions**, so it satisfies both the "Visual Basic + Oracle" brief and
the "open it in any browser" brief:

| Deliverable | Folder | Purpose |
|---|---|---|
| **Production application** | [`src/`](src/) | ASP.NET **Web Forms (VB.NET)** + **Oracle** (ODP.NET). The real, deployable system. |
| **Web edition** | [`webapp/`](webapp/) | Same modules, same tax engine, data kept in the browser. Runs with no server. |
| **Deployable build** | [`dist/`](dist/) | The web edition inlined into **one self-contained `index.html`** — drop it on any static host. |
| **Oracle database** | [`database/`](database/) | Schema DDL, seed data, audit triggers, report views. |
| **Documentation** | [`docs/`](docs/) | [User & Feature Guide](docs/User-Guide.pdf) · [The Code, Explained](docs/Code-Explained.pdf) |
| **Demo video** | [`demo-video/`](demo-video/) | Narrated MP4 walkthrough + slide deck + script. |

Both editions implement the **same seven modules, the same five-table data model and the same
tax computation** — the web edition simply stores data in the browser (`localStorage`).

---

## 2. Modules (mapped to the SRS)

1. **Client Information** — add / update / delete clients; PAN is the validated primary key.
2. **Original Return** — file the original return for an assessment year; tax computed automatically.
3. **Revised Return** — file a correction; the system enforces that an original return already exists.
4. **Trading Account** *(firms)* — debit/credit sides with automatic balancing.
5. **Profit & Loss Account** *(firms)* — full expense/income ledger with balancing.
6. **Balance Sheet** *(firms)* — assets vs. liabilities & capital with balancing.
7. **Report Generation** — statutory reports (return history, returns in a fiscal, revised returns),
   printable to PDF.

Security: forms-based login, SHA-256 password hashes, and Oracle audit triggers logging every
insert/update/delete with user, table and timestamp.

---

## 3. Technology stack

| Layer | Production (`src/`) | Web edition (`webapp/`) |
|---|---|---|
| UI | ASP.NET Web Forms (`.aspx`) | HTML5 + CSS3 (responsive, light/dark) |
| Language | **VB.NET** | Vanilla JavaScript |
| Data access | ODP.NET Managed (`Oracle.ManagedDataAccess`) | `localStorage` |
| Database | **Oracle** 12c+ / XE / Autonomous DB | in-browser |
| Tax engine | `TaxEngine.vb` | `tax.js` (identical logic) |
| Runtime | .NET Framework 4.8 / IIS | any modern browser |

---

## 4. Run the web edition locally (no build)

```bash
cd webapp
python3 -m http.server 8080     # open http://localhost:8080
```

Use the **🧭 guided tour** for a walkthrough and **🌓** to toggle light/dark.
Run `TaxSystem.reset()` in the browser console to restore the sample data.

### Rebuild the single-file deployable

```bash
python3 demo-video/build-standalone.py    # -> dist/index.html (self-contained, ~87 KB)
```

### Publish it (any static host)

`dist/index.html` has **no external dependencies**, so it works anywhere:

| Host | How |
|---|---|
| **Netlify** | Log in → drag the `dist` folder onto <https://app.netlify.com/drop> → rename the site. Or `netlify deploy --prod --dir=dist`. |
| **Vercel** | `vercel deploy --prod dist` |
| **GitHub Pages** | Push `dist/` to a repo and enable Pages. |
| **Hugging Face Spaces** | Create a **Static** Space and upload `index.html`. |

---

## 5. Run the production app (VB.NET + Oracle)

### Prerequisites
Windows with **IIS / IIS Express**, **Visual Studio 2019/2022**, **.NET Framework 4.8**, and an
**Oracle** database (local **XE 21c**, or a free **Oracle Autonomous Database**).

### Step 1 — Create the database
Run the scripts in [`database/`](database/) **in order**:

```sql
@01_create_user.sql        -- as SYSTEM/ADMIN: creates the ITEMS schema user
-- then connect as that user:
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

For Autonomous DB, download the wallet, set `TNS_ADMIN` to the wallet folder, and use the TNS alias.

### Step 3 — Build & run
```powershell
cd src
nuget restore ITEMS.sln
msbuild ITEMS.sln /p:Configuration=Debug
```
Press **F5** in Visual Studio, or host on IIS. Sign in with `admin / admin@123`.

---

## 6. Directory structure

```
Income-Tax-Evaluation-System/
├── README.md
├── dist/index.html            ← self-contained deployable (drop on any host)
├── webapp/                    ← web edition source
│   ├── index.html · css/styles.css
│   └── js/  (tax.js · db.js · app.js)
├── src/                       ← production ASP.NET Web Forms (VB.NET)
│   ├── ITEMS.sln
│   └── ITEMS/
│       ├── Web.config · Site.Master(+.vb/.designer.vb)
│       ├── Login / Default / Clients / ClientEdit
│       ├── Returns / ReturnEdit / FirmAccount / Reports  (.aspx + .vb + .designer.vb)
│       └── App_Code/  (OracleDb · Models · TaxEngine · Security · *Repository)
├── database/                  ← Oracle SQL scripts (run 01→04)
├── docs/                      ← User-Guide.pdf · Code-Explained.pdf · screenshots/
└── demo-video/                ← narrated MP4 + slides + narration + build scripts
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

Then: rebate u/s 87A (income ≤ ₹5,00,000), surcharge (10/15/25/37% by band), 4% health & education
cess, less TDS / advance / self-assessment tax → **balance payable or refund**.
The same logic lives in `tax.js` and `TaxEngine.vb` — a ₹12,00,000 salary yields **₹1,79,400** in both.

> ⚠️ Figures are illustrative for demonstration and training; verify against the current
> Finance Act before any real filing. Change the demo passwords before any real deployment.

---

## 8. Documentation

- **[User & Feature Guide](docs/User-Guide.pdf)** — every screen and feature, with screenshots.
- **[The Code, Explained](docs/Code-Explained.pdf)** — a line-by-line walkthrough of the code
  written for readers with **no programming background**, plus the full code-review log.

---

## 9. Credits

Re-engineered from the *Income Tax Evaluation & Maintenance System* project report
(`18.Utilities/Project/project.pdf`). Original concept: VC++ 6.0 + Oracle 8i; this edition
modernises it to VB.NET + Oracle with a browser-accessible web edition.
