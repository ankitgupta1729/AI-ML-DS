/* =============================================================================
 * Income Tax Evaluation System · app.js — SPA router, views and module logic
 * ===========================================================================*/
(function (global) {
  "use strict";
  const DB = global.TaxDB, TAX = global.TaxEngine;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const el = (h) => { const t = document.createElement("template"); t.innerHTML = h.trim(); return t.content.firstElementChild; };

  /* ---- Formatting --------------------------------------------------------- */
  const inr = (v) => "₹" + Number(v || 0).toLocaleString("en-IN");
  const inr2 = (v) => "₹" + Number(v || 0).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const fyLabel = (r) => `AY ${String(r.ASSES_YEAR_1).slice(0,4)}-${String(r.ASSES_YEAR_2).slice(2,4)}`;
  const fmtDate = (d) => { if (!d) return "—"; const x = new Date(d); return isNaN(x) ? d : x.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }); };
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[c]));

  const humanize = (k) => {
    const over = { TO_POST_TLGRM_FAX_COUR_PH: "Postage, Telegram, Fax etc.", TO_MANU_ASSEM_EXPEN: "Manufacturing & Assembling Exp.",
      TO_DRCT_FACT_PROD_EXP: "Direct Factory Productive Exp.", TO_MISC_SUNDRY_EXPENSE: "Miscellaneous & Sundry Exp.",
      TO_LIGHT_WATER_ELECT: "Lighting, Water & Electricity", TO_STAFF_WELF_EXPENSE: "Staff Welfare Expenses",
      TO_ESTAB_EXPENSE: "Establishment Expenses", TO_IMPORT_DUTY_CUSTOMS: "Import Duty & Customs",
      TO_HEATING_LIGHTING_POWER: "Heating, Lighting & Power", TO_COAL_WATER_GAS: "Coal, Water & Gas",
      TO_LOSS_ON_SALE_OF_ASSET: "Loss on Sale of Assets", TO_LOSS_BY_THEFT_ACCIDENT: "Loss by Fire/Theft/Accident",
      BY_PROF_FROM_SALE_OF_ASSET: "Profit from Sale of Assets", BY_INC_IN_VALUE_OF_ASSET: "Increase in Value of Assets",
      BY_RES_FOR_BAD_DOUBTS: "Reserve for Bad Doubts", BY_APPRENTICESHIP_PREMIUM: "Apprenticeship Premium",
      PLANT_AND_MACHINERY: "Plant & Machinery" };
    if (over[k]) return over[k];
    return k.replace(/^TO_|^BY_/, "").replace(/_/g, " ").toLowerCase()
      .replace(/\b\w/g, c => c.toUpperCase()).replace(/\bAnd\b/g, "&").replace(/Pl\b/, "P&L");
  };

  /* ---- Toast / modal ------------------------------------------------------ */
  function toast(title, sub, type) {
    let wrap = $(".toast-wrap"); if (!wrap) { wrap = el(`<div class="toast-wrap"></div>`); document.body.appendChild(wrap); }
    const t = el(`<div class="toast ${type||""}"><b>${esc(title)}</b>${sub?`<small>${esc(sub)}</small>`:""}</div>`);
    wrap.appendChild(t); setTimeout(() => { t.style.opacity = "0"; setTimeout(() => t.remove(), 300); }, 3200);
  }
  function confirmModal(title, body, okLabel, onOk, danger) {
    const back = el(`<div class="modal-back"><div class="modal">
      <div class="m-head"><h3>${esc(title)}</h3></div>
      <div class="m-body">${body}</div>
      <div class="m-foot"><button class="btn btn-ghost" data-x>Cancel</button>
      <button class="btn ${danger?"btn-danger":"btn-primary"}" data-ok>${esc(okLabel)}</button></div></div></div>`);
    document.body.appendChild(back);
    const close = () => back.remove();
    back.addEventListener("click", e => { if (e.target === back) close(); });
    $("[data-x]", back).onclick = close;
    $("[data-ok]", back).onclick = () => { close(); onOk(); };
  }

  /* ---- Theme -------------------------------------------------------------- */
  function applyTheme(t) { document.documentElement.setAttribute("data-theme", t); localStorage.setItem("items_theme", t); }
  applyTheme(localStorage.getItem("items_theme") || "light");
  function toggleTheme() { applyTheme(document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark"); }

  /* =========================================================================
   * AUTH
   * =======================================================================*/
  function renderLogin() {
    document.body.innerHTML = "";
    const wrap = el(`<div class="login-wrap"><div class="login-card">
      <div class="login-head">
        <div class="logo"><span class="mark">₹</span> Income Tax Evaluation System</div>
        <h1>Sign in to your workspace</h1>
        <p>Client records &middot; Return filing &middot; Firm accounts &middot; Reports</p>
      </div>
      <form class="login-body" id="loginForm" autocomplete="off">
        <div class="field"><label>User ID <span class="req">*</span></label>
          <input id="u" placeholder="e.g. admin" required></div>
        <div class="field"><label>Password <span class="req">*</span></label>
          <input id="p" type="password" placeholder="Enter password" required></div>
        <div class="err-text" id="loginErr"></div>
        <button class="btn btn-primary" style="width:100%" type="submit">Sign in &rarr;</button>
        <div class="hint">Demo credentials &mdash; Admin: <code>admin</code> / <code>admin@123</code> &nbsp;·&nbsp;
          Operator: <code>operator</code> / <code>demo@2025</code></div>
      </form></div></div>`);
    document.body.appendChild(wrap);
    $("#loginForm").addEventListener("submit", (e) => {
      e.preventDefault();
      const s = DB.login($("#u").value.trim(), $("#p").value);
      if (!s) { $("#loginErr").textContent = "Invalid user id or password. Please try again."; return; }
      location.hash = "#/dashboard"; boot();
    });
  }

  /* =========================================================================
   * SHELL
   * =======================================================================*/
  const NAV = [
    { group: "Overview" },
    { id: "dashboard", icon: "📊", label: "Dashboard" },
    { group: "Master" },
    { id: "clients", icon: "👤", label: "Client Information" },
    { group: "Transactions" },
    { id: "returns", icon: "📄", label: "Return Filing" },
    { id: "trading", icon: "📦", label: "Trading Account" },
    { id: "pl", icon: "💹", label: "Profit & Loss A/c" },
    { id: "balance", icon: "⚖️", label: "Balance Sheet" },
    { group: "Output" },
    { id: "reports", icon: "🗂️", label: "Reports" }
  ];

  function renderShell() {
    const s = DB.session();
    document.body.innerHTML = "";
    const app = el(`<div class="app">
      <aside class="sidebar" id="sidebar">
        <div class="brand"><span class="mark">₹</span><div><b>Income Tax</b><small>Evaluation System</small></div></div>
        <nav class="nav" id="nav"></nav>
        <div style="padding:.8rem 1rem;border-top:1px solid var(--line);font-size:.72rem;color:var(--muted)">
          v1.0 &middot; Demo build<br>Data stored locally in your browser</div>
      </aside>
      <div class="main">
        <header class="topbar">
          <button class="icon-btn hamburger" id="ham" aria-label="Menu">☰</button>
          <div class="crumbs" id="crumbs">Dashboard<small>Welcome back</small></div>
          <div class="spacer"></div>
          <button class="icon-btn no-print" id="tourBtn" title="Guided tour">🧭</button>
          <button class="icon-btn no-print" id="themeBtn" title="Toggle theme">🌓</button>
          <div class="user-chip"><span class="av">${esc((s.name||"U").slice(0,1))}</span>
            <div><b style="font-size:.82rem">${esc(s.name)}</b><small>${esc(s.role)}</small></div>
            <button class="icon-btn" id="logout" title="Sign out">⏻</button></div>
        </header>
        <div class="content" id="view"></div>
      </div>
    </div>`);
    document.body.appendChild(app);

    const nav = $("#nav");
    NAV.forEach(n => {
      if (n.group) nav.appendChild(el(`<div class="group">${esc(n.group)}</div>`));
      else nav.appendChild(el(`<a href="#/${n.id}" data-nav="${n.id}"><span class="ico">${n.icon}</span>${esc(n.label)}</a>`));
    });
    $("#logout").onclick = () => confirmModal("Sign out?", "You will be returned to the login screen.", "Sign out",
      () => { DB.logout(); location.hash = ""; renderLogin(); });
    $("#themeBtn").onclick = toggleTheme;
    $("#tourBtn").onclick = startTour;
    $("#ham").onclick = () => $("#sidebar").classList.toggle("open");
    nav.addEventListener("click", () => $("#sidebar").classList.remove("open"));
  }

  function setCrumbs(title, sub) {
    const c = $("#crumbs"); if (c) c.innerHTML = `${esc(title)}<small>${esc(sub||"")}</small>`;
    $$("#nav a").forEach(a => a.classList.remove("active"));
  }
  function markNav(id) { const a = $(`#nav a[data-nav="${id}"]`); if (a) a.classList.add("active"); }

  /* =========================================================================
   * DASHBOARD
   * =======================================================================*/
  function viewDashboard(view) {
    setCrumbs("Dashboard", "Practice overview"); markNav("dashboard");
    const clients = DB.all("CLIENT_RECORD"), returns = DB.all("INCOME_TAX_RECORD");
    const firms = clients.filter(c => Number(c.INDV_HUF_FIRM_AOP_LA) === 2).length;
    const revised = returns.filter(r => Number(r.RETURN_ORIGINAL_REVISED) === 1).length;
    const totalTax = returns.reduce((a, r) => a + Number(r.NET_TAX_PAYABLE || 0), 0);
    const byFiscal = {};
    returns.forEach(r => { const k = fyLabel(r); byFiscal[k] = (byFiscal[k] || 0) + 1; });
    const fiscals = Object.keys(byFiscal).sort();
    const maxF = Math.max(1, ...Object.values(byFiscal));

    view.innerHTML = `
      <div class="page-head"><div><h2>Welcome back</h2>
        <p class="muted">A consolidated view of clients, returns and tax collections.</p></div>
        <div class="btn-row no-print"><a class="btn btn-ghost" href="#/reports">View reports</a>
          <a class="btn btn-primary" href="#/clients/new">+ New client</a></div></div>
      <div class="grid grid-4" style="margin-bottom:1.2rem">
        <div class="stat i1"><div class="ico">👥</div><div class="lbl">Total Clients</div>
          <div class="val mono">${clients.length}</div><div class="sub">${firms} firm(s) · ${clients.length-firms} individual(s)</div></div>
        <div class="stat i2"><div class="ico">📄</div><div class="lbl">Returns Filed</div>
          <div class="val mono">${returns.length}</div><div class="sub">${returns.length-revised} original · ${revised} revised</div></div>
        <div class="stat i3"><div class="ico">🔁</div><div class="lbl">Revised Returns</div>
          <div class="val mono">${revised}</div><div class="sub">Corrections to original filings</div></div>
        <div class="stat i4"><div class="ico">💰</div><div class="lbl">Net Tax (recorded)</div>
          <div class="val mono">${inr(totalTax)}</div><div class="sub">Across all assessment years</div></div>
      </div>
      <div class="grid grid-2">
        <div class="card"><div class="card-head"><h3>Returns by Assessment Year</h3></div>
          <div class="card-body"><div id="bars" style="display:flex;flex-direction:column;gap:.7rem">
          ${fiscals.map(f => `<div><div style="display:flex;justify-content:space-between;font-size:.84rem;margin-bottom:.2rem">
            <span>${esc(f)}</span><b class="mono">${byFiscal[f]}</b></div>
            <div style="height:12px;background:var(--surface-2);border-radius:99px;overflow:hidden">
            <div style="height:100%;width:${(byFiscal[f]/maxF*100).toFixed(0)}%;background:var(--brand-grad);border-radius:99px"></div>
            </div></div>`).join("") || `<p class="muted">No returns yet.</p>`}
          </div></div></div>
        <div class="card"><div class="card-head"><h3>Recent Returns</h3><a class="btn btn-sm btn-ghost no-print" href="#/returns">All &rarr;</a></div>
          <div class="card-body" style="padding:0"><div class="table-wrap"><table class="data"><thead><tr>
          <th>Client</th><th>AY</th><th>Type</th><th class="num">Total Income</th></tr></thead><tbody>
          ${returns.slice().reverse().slice(0,6).map(r => { const c = DB.findClient(r.PAN);
            return `<tr><td>${esc(c?c.CLIENT_NAME:r.PAN)}</td><td>${esc(fyLabel(r))}</td>
              <td><span class="badge ${Number(r.RETURN_ORIGINAL_REVISED)?"badge-revised":"badge-original"}">${Number(r.RETURN_ORIGINAL_REVISED)?"Revised":"Original"}</span></td>
              <td class="num mono">${inr(r.TOTAL_INCOME)}</td></tr>`; }).join("") ||
            `<tr><td colspan="4" class="empty">No returns filed.</td></tr>`}
          </tbody></table></div></div></div>
      </div>`;
  }

  /* =========================================================================
   * CLIENT MODULE
   * =======================================================================*/
  function viewClients(view) {
    setCrumbs("Client Information", "Master records"); markNav("clients");
    const render = (q) => {
      let rows = DB.all("CLIENT_RECORD");
      if (q) { q = q.toLowerCase(); rows = rows.filter(c => (c.CLIENT_NAME+c.PAN+c.ADDRESS).toLowerCase().includes(q)); }
      const body = rows.length ? rows.map(c => `<tr>
        <td class="mono">${esc(c.PAN)}</td><td><b>${esc(c.CLIENT_NAME)}</b><br><small class="muted">${esc(c.FATHERS_NAME)}</small></td>
        <td><span class="badge ${Number(c.INDV_HUF_FIRM_AOP_LA)===2?"badge-firm":"badge-indv"}">${esc(DB.CATEGORY[c.INDV_HUF_FIRM_AOP_LA])}</span></td>
        <td>${esc(fmtDate(c.DOB))}</td><td>${esc(c.WARD_CIRCLE_SPECIAL_RANGE)}</td>
        <td class="no-print"><div class="row-actions">
          <a class="btn btn-sm btn-ghost" href="#/clients/edit/${encodeURIComponent(c.PAN)}">Edit</a>
          <button class="btn btn-sm btn-danger" data-del="${esc(c.PAN)}">Delete</button></div></td></tr>`).join("")
        : `<tr><td colspan="6"><div class="empty"><div class="big">👤</div>No clients found. Add your first client to begin.</div></td></tr>`;
      $("#clientBody").innerHTML = body;
      $$("#clientBody [data-del]").forEach(b => b.onclick = () => {
        const pan = b.getAttribute("data-del"); const c = DB.findClient(pan);
        confirmModal("Delete client?", `This will permanently remove <b>${esc(c.CLIENT_NAME)}</b> (${esc(pan)}) and all linked returns, trading, P&amp;L and balance-sheet records.`,
          "Delete", () => { DB.deleteClient(pan); toast("Client deleted", c.CLIENT_NAME); render($("#cSearch").value); }, true);
      });
    };
    view.innerHTML = `
      <div class="page-head"><div><h2>Client Information</h2>
        <p class="muted">Add, update and remove clients. PAN is the unique primary key.</p></div>
        <a class="btn btn-primary no-print" href="#/clients/new">+ Insert Client Record</a></div>
      <div class="toolbar no-print"><div class="search"><span class="mag">🔍</span>
        <input id="cSearch" placeholder="Search by name, PAN or address..."></div></div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr>
        <th>PAN</th><th>Name / Father</th><th>Category</th><th>Date of Birth</th><th>Ward/Circle</th><th class="no-print">Actions</th>
        </tr></thead><tbody id="clientBody"></tbody></table></div></div>`;
    render("");
    $("#cSearch").addEventListener("input", (e) => render(e.target.value));
  }

  function viewClientForm(view, mode, pan) {
    const editing = mode === "edit";
    const rec = editing ? DB.findClient(pan) : DB.mkClient({ PAN: "" });
    if (editing && !rec) { toast("Not found", "Client does not exist", "err"); location.hash = "#/clients"; return; }
    setCrumbs(editing ? "Update Client" : "Insert Client", "Client Information module"); markNav("clients");

    view.innerHTML = `
      <div class="page-head"><div><h2>${editing?"Update":"Insert"} Client Record</h2>
        <p class="muted">${editing?"Modify the details of "+esc(rec.CLIENT_NAME):"Enter the basic information of a new client."}</p></div>
        <a class="btn btn-ghost no-print" href="#/clients">&larr; Back to list</a></div>
      <div class="card"><div class="card-body"><form id="cForm" autocomplete="off"><div class="form-grid">
        <div class="section-title">Identification</div>
        <div class="field"><label>PAN <span class="req">*</span></label>
          <input id="PAN" maxlength="10" value="${esc(rec.PAN)}" ${editing?"readonly":""} placeholder="ABCDE1234F" style="text-transform:uppercase">
          <div class="err-text" data-err="PAN"></div></div>
        <div class="field"><label>Full Name <span class="req">*</span></label>
          <input id="CLIENT_NAME" maxlength="30" value="${esc(rec.CLIENT_NAME)}"><div class="err-text" data-err="CLIENT_NAME"></div></div>
        <div class="field"><label>Father's Name</label>
          <input id="FATHERS_NAME" maxlength="30" value="${esc(rec.FATHERS_NAME)}"></div>
        <div class="field"><label>Date of Birth</label>
          <input id="DOB" type="date" value="${esc(rec.DOB)}"></div>
        <div class="section-title">Contact</div>
        <div class="field full"><label>Address</label>
          <textarea id="ADDRESS" maxlength="60">${esc(rec.ADDRESS)}</textarea></div>
        <div class="field"><label>PIN Code</label>
          <input id="PINCODE" maxlength="6" value="${esc(rec.PINCODE)}" placeholder="6 digits"><div class="err-text" data-err="PINCODE"></div></div>
        <div class="field"><label>Telephone</label>
          <input id="TELEPHONE" maxlength="15" value="${esc(rec.TELEPHONE)}"><div class="err-text" data-err="TELEPHONE"></div></div>
        <div class="section-title">Classification</div>
        <div class="field"><label>Category (I / HUF / Firm / AOP / LA)</label>
          <div class="radio-row" id="cat">${DB.CATEGORY.map((c,i)=>`<label><input type="radio" name="cat" value="${i}" ${i==rec.INDV_HUF_FIRM_AOP_LA?"checked":""}>${esc(c)}</label>`).join("")}</div></div>
        <div class="field"><label>Residential Status</label>
          <div class="radio-row" id="res">${DB.RESIDENCE.map((c,i)=>`<label><input type="radio" name="res" value="${i}" ${i==rec.RESIDENT_NR_NOR?"checked":""}>${esc(c)}</label>`).join("")}</div></div>
        <div class="field"><label>Sex</label>
          <div class="radio-row" id="sex"><label><input type="radio" name="sex" value="1" ${rec.SEX==1?"checked":""}>Male</label>
            <label><input type="radio" name="sex" value="0" ${rec.SEX==0?"checked":""}>Female</label></div></div>
        <div class="field"><label>Ward / Circle / Special Range</label>
          <input id="WARD_CIRCLE_SPECIAL_RANGE" maxlength="20" value="${esc(rec.WARD_CIRCLE_SPECIAL_RANGE)}"></div>
      </div>
      <div class="btn-row no-print" style="margin-top:1rem">
        <button class="btn btn-primary" type="submit">${editing?"💾 Update":"💾 Save"} Client</button>
        <a class="btn btn-ghost" href="#/clients">Cancel</a></div></form></div></div>`;

    $("#cForm").addEventListener("submit", (e) => {
      e.preventDefault();
      const val = (id) => $("#"+id).value.trim();
      const errs = {};
      const panV = val("PAN").toUpperCase();
      if (!editing) {
        if (!/^[A-Z]{5}[0-9]{4}[A-Z]$/.test(panV)) errs.PAN = "PAN must match format ABCDE1234F.";
        else if (DB.findClient(panV)) errs.PAN = "A client with this PAN already exists.";
      }
      if (!val("CLIENT_NAME")) errs.CLIENT_NAME = "Name is required.";
      if (val("PINCODE") && !/^[0-9]{6}$/.test(val("PINCODE"))) errs.PINCODE = "PIN code must be 6 digits.";
      if (val("TELEPHONE") && !/^[0-9+\-\s]{6,15}$/.test(val("TELEPHONE"))) errs.TELEPHONE = "Enter a valid phone number.";
      $$("[data-err]").forEach(n => n.textContent = "");
      $$("#cForm input, #cForm textarea").forEach(n => n.classList.remove("invalid"));
      if (Object.keys(errs).length) {
        Object.entries(errs).forEach(([k,v]) => { const e2 = $(`[data-err="${k}"]`); if (e2) e2.textContent = v; const inp = $("#"+k); if (inp) inp.classList.add("invalid"); });
        toast("Please fix the highlighted fields", "", "err"); return;
      }
      const out = DB.mkClient({
        PAN: editing ? rec.PAN : panV, CLIENT_NAME: val("CLIENT_NAME"), FATHERS_NAME: val("FATHERS_NAME"),
        DOB: val("DOB"), ADDRESS: val("ADDRESS"), PINCODE: val("PINCODE"), TELEPHONE: val("TELEPHONE"),
        SEX: +($('input[name="sex"]:checked')?.value ?? 1),
        INDV_HUF_FIRM_AOP_LA: +($('input[name="cat"]:checked')?.value ?? 0),
        RESIDENT_NR_NOR: +($('input[name="res"]:checked')?.value ?? 0),
        WARD: val("WARD_CIRCLE_SPECIAL_RANGE") || "Ward"
      });
      DB.upsertClient(out);
      toast(editing ? "Client updated" : "Client saved", out.CLIENT_NAME);
      location.hash = "#/clients";
    });
  }

  /* =========================================================================
   * RETURN MODULE (Original / Revised) + tax computation
   * =======================================================================*/
  function viewReturns(view) {
    setCrumbs("Return Filing", "Original & Revised returns"); markNav("returns");
    const render = (q) => {
      let rows = DB.all("INCOME_TAX_RECORD");
      if (q) { q = q.toLowerCase(); rows = rows.filter(r => { const c = DB.findClient(r.PAN); return ((c?c.CLIENT_NAME:"")+r.PAN+fyLabel(r)).toLowerCase().includes(q); }); }
      $("#rBody").innerHTML = rows.length ? rows.map(r => { const c = DB.findClient(r.PAN); const rev = Number(r.RETURN_ORIGINAL_REVISED);
        return `<tr><td class="mono">${esc(r.PAN)}</td><td><b>${esc(c?c.CLIENT_NAME:"—")}</b></td>
        <td>${esc(fyLabel(r))}</td>
        <td><span class="badge ${rev?"badge-revised":"badge-original"}">${rev?"Revised":"Original"}</span></td>
        <td class="num mono">${inr(r.TOTAL_INCOME)}</td><td class="num mono">${inr(r.NET_TAX_PAYABLE)}</td>
        <td class="num mono">${Number(r.BAL_TAX_PAYABLE_REFUND)<0?'<span style="color:var(--ok)">'+inr(-r.BAL_TAX_PAYABLE_REFUND)+' Ref</span>':inr(r.BAL_TAX_PAYABLE_REFUND)}</td>
        <td class="no-print"><div class="row-actions">
          <a class="btn btn-sm btn-ghost" href="#/returns/edit/${encodeURIComponent(DB.returnKey(r))}">Edit</a>
          <button class="btn btn-sm btn-danger" data-del="${esc(DB.returnKey(r))}">Delete</button></div></td></tr>`; }).join("")
        : `<tr><td colspan="8"><div class="empty"><div class="big">📄</div>No returns filed yet.</div></td></tr>`;
      $$("#rBody [data-del]").forEach(b => b.onclick = () => {
        const key = b.getAttribute("data-del"); const rec = DB.all("INCOME_TAX_RECORD").find(x => DB.returnKey(x)===key);
        confirmModal("Delete return?", `Delete this ${Number(rec.RETURN_ORIGINAL_REVISED)?"revised":"original"} return for ${esc(rec.PAN)} (${esc(fyLabel(rec))})?`,
          "Delete", () => { DB.deleteReturn(rec); toast("Return deleted"); render($("#rSearch").value); }, true);
      });
    };
    view.innerHTML = `
      <div class="page-head"><div><h2>Return Filing</h2>
        <p class="muted">File original returns, revise mistakes, and let the engine compute the tax.</p></div>
        <a class="btn btn-primary no-print" href="#/returns/new">+ File New Return</a></div>
      <div class="toolbar no-print"><div class="search"><span class="mag">🔍</span>
        <input id="rSearch" placeholder="Search by client, PAN or assessment year..."></div></div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr>
        <th>PAN</th><th>Client</th><th>AY</th><th>Type</th><th class="num">Total Income</th>
        <th class="num">Net Tax</th><th class="num">Balance</th><th class="no-print">Actions</th>
        </tr></thead><tbody id="rBody"></tbody></table></div></div>`;
    render("");
    $("#rSearch").addEventListener("input", e => render(e.target.value));
  }

  function viewReturnForm(view, mode, key) {
    const editing = mode === "edit";
    const clients = DB.all("CLIENT_RECORD");
    if (!clients.length) { view.innerHTML = `<div class="empty"><div class="big">👤</div>Add a client first before filing a return.
      <div style="margin-top:1rem"><a class="btn btn-primary" href="#/clients/new">+ Add client</a></div></div>`; return; }
    let rec = editing ? DB.all("INCOME_TAX_RECORD").find(r => DB.returnKey(r) === key) : DB.mkReturn({ PAN: clients[0].PAN });
    if (editing && !rec) { location.hash = "#/returns"; return; }
    rec = Object.assign({}, rec);
    setCrumbs(editing ? "Edit Return" : "File Return", "Return Information module"); markNav("returns");

    const incomeFields = [
      ["INCOME_FROM_SALARY", "Income from Salary"], ["INCOME_FROM_HOUSE_PROPERTY", "Income from House Property"],
      ["INCOME_FROM_BUSINESS", "Income from Business / Profession"], ["TOTAL_SHORT_TERM_GAIN", "Short-term Capital Gain"],
      ["TOTAL_LONG_TERM_GAIN", "Long-term Capital Gain"], ["INCOME_FROM_OTHER_SOURCES", "Income from Other Sources"],
      ["INCM_OTHER_PERS_TO_ADDED", "Income of Other Person (clubbed)"], ["LESS_DEDUCTION_UNDER_VIA", "Less: Deductions (Chapter VI-A)"]
    ];
    const payFields = [
      ["TAX_DEDUC_AT_SOURCE", "Tax Deducted at Source (TDS)"], ["ADVANCE_TAX_PAID", "Advance Tax Paid"],
      ["TOT_SELF_ASSESS_TAX_PAID", "Self-Assessment Tax Paid"], ["INTEREST_PAYABLE", "Interest Payable (234A/B/C)"],
      ["LESS_RELIEF", "Less: Relief u/s 89/90/91"]
    ];

    view.innerHTML = `
      <div class="page-head"><div><h2>${editing?"Edit":"File"} Income Tax Return</h2>
        <p class="muted">Verify the client via PAN, enter income heads, and compute the tax liability.</p></div>
        <a class="btn btn-ghost no-print" href="#/returns">&larr; Back</a></div>
      <div class="grid" style="grid-template-columns:1.6fr 1fr;gap:1.1rem" id="rGrid">
        <div class="card"><div class="card-body"><form id="rForm"><div class="form-grid">
          <div class="section-title">Return header</div>
          <div class="field"><label>Client (PAN) <span class="req">*</span></label>
            <select id="PAN" ${editing?"disabled":""}>${clients.map(c=>`<option value="${esc(c.PAN)}" ${c.PAN===rec.PAN?"selected":""}>${esc(c.CLIENT_NAME)} — ${esc(c.PAN)}</option>`).join("")}</select></div>
          <div class="field"><label>Return Type</label>
            <div class="radio-row" id="rt"><label><input type="radio" name="rt" value="0" ${!Number(rec.RETURN_ORIGINAL_REVISED)?"checked":""}>Original</label>
            <label><input type="radio" name="rt" value="1" ${Number(rec.RETURN_ORIGINAL_REVISED)?"checked":""}>Revised</label></div>
            <div class="err-text" data-err="rt"></div></div>
          <div class="field"><label>Assessment Year — From</label>
            <input id="AY1" type="date" value="${esc(rec.ASSES_YEAR_1)}" ${editing?"readonly":""}></div>
          <div class="field"><label>Assessment Year — To</label>
            <input id="AY2" type="date" value="${esc(rec.ASSES_YEAR_2)}" ${editing?"readonly":""}></div>
          <div class="section-title">Income heads</div>
          ${incomeFields.map(([k,l]) => `<div class="field"><label>${esc(l)}</label>
            <input class="calc" data-k="${k}" type="number" min="0" step="1" value="${Number(rec[k])||""}" placeholder="0"></div>`).join("")}
          <div class="section-title">Taxes already paid</div>
          ${payFields.map(([k,l]) => `<div class="field"><label>${esc(l)}</label>
            <input class="calc" data-k="${k}" type="number" min="0" step="1" value="${Number(rec[k])||""}" placeholder="0"></div>`).join("")}
        </div>
        <div class="btn-row no-print" style="margin-top:1rem">
          <button class="btn btn-primary" type="submit">💾 ${editing?"Update":"File"} Return</button>
          <a class="btn btn-ghost" href="#/returns">Cancel</a></div></form></div></div>
        <div><div class="card" style="position:sticky;top:76px"><div class="card-head"><h3>Computation of Tax</h3>
          <span class="pill" id="regimePill">Old regime</span></div>
          <div class="card-body" id="computed"></div></div></div>
      </div>`;

    const readForm = () => {
      const o = Object.assign({}, rec);
      $$("#rForm .calc").forEach(i => o[i.getAttribute("data-k")] = Number(i.value) || 0);
      o.PAN = $("#PAN").value;
      o.RETURN_ORIGINAL_REVISED = +($('input[name="rt"]:checked')?.value ?? 0);
      o.ASSES_YEAR_1 = $("#AY1").value; o.ASSES_YEAR_2 = $("#AY2").value;
      return o;
    };
    const recompute = () => {
      const o = readForm(); const client = DB.findClient(o.PAN);
      const comp = TAX.compute(o, client);
      $("#regimePill").textContent = Number(client?.INDV_HUF_FIRM_AOP_LA) === 2 ? "Firm @ 30%" : "Old regime";
      const line = (l, v, strong, hl) => `<div class="lrow" style="${strong?'font-weight:800;':''}">
        <span style="${hl?'color:var(--brand)':''}">${esc(l)}</span><span class="amt" style="${hl?'color:var(--brand)':''}">${inr(v)}</span></div>`;
      const bal = comp.BAL_TAX_PAYABLE_REFUND;
      $("#computed").innerHTML =
        line("Gross Total Income", comp.GROSS_TOTAL_INCOME) +
        line("Less: Deductions VI-A", Number(o.LESS_DEDUCTION_UNDER_VIA)) +
        line("Total Income", comp.TOTAL_INCOME, true, true) +
        `<div style="height:.5rem"></div>` +
        line("Tax at normal rates", comp.INCOME_TAX_NORM_RATE) +
        line("Tax at special rates", comp.INCOME_TAX_SPCL_RATE) +
        line("Tax on Total Income", comp.TAX_ON_TOTAL_INCOME) +
        line("Less: Rebate u/s 87A", comp.LESS_REBATE) +
        line("Add: Surcharge", comp.ADDITIONAL_SURCHARGE) +
        line("Add: Health & Edu Cess (4%)", comp.TOTAL_TAX_PAYABLE - comp.TAX_PAYABLE - comp.ADDITIONAL_SURCHARGE) +
        line("Total Tax Payable", comp.TOTAL_TAX_PAYABLE, true) +
        line("Net Tax Payable", comp.NET_TAX_PAYABLE, true, true) +
        `<div class="total" style="border-top:2px dashed var(--line);margin-top:.6rem">
          <span>${bal < 0 ? "Refund Due" : "Balance Payable"}</span>
          <span class="${bal<0?'balanced':''}">${inr(Math.abs(bal))}</span></div>`;
    };
    recompute();
    $$("#rForm .calc, #PAN, input[name='rt']").forEach(i => i.addEventListener("input", recompute));

    $("#rForm").addEventListener("submit", (e) => {
      e.preventDefault();
      const o = readForm();
      if (!o.ASSES_YEAR_1 || !o.ASSES_YEAR_2) { toast("Assessment year is required", "", "err"); return; }
      const isRevised = Number(o.RETURN_ORIGINAL_REVISED) === 1;
      if (!editing && isRevised && !DB.hasOriginal(o.PAN, o.ASSES_YEAR_1, o.ASSES_YEAR_2)) {
        $(`[data-err="rt"]`).textContent = "An original return must be filed before a revised one (per SRS rule).";
        toast("Cannot file revised return", "No original return exists for this AY", "err"); return;
      }
      Object.assign(o, TAX.compute(o, DB.findClient(o.PAN)));
      DB.upsertReturn(o);
      toast(editing ? "Return updated" : (isRevised ? "Revised return filed" : "Original return filed"),
        DB.findClient(o.PAN)?.CLIENT_NAME);
      location.hash = "#/returns";
    });
  }

  /* =========================================================================
   * LEDGER MODULES (Trading / P&L / Balance Sheet)
   * =======================================================================*/
  const LEDGERS = {
    trading: { table: "TRADING_ACCOUNT", title: "Trading Account", icon: "📦",
      fields: DB.TRADING_FIELDS, leftPrefix: "TO_", rightPrefix: "BY_",
      leftHead: "Dr. (To)", rightHead: "Cr. (By)", firmOnly: true },
    pl: { table: "PL_ACCOUNT", title: "Profit & Loss Account", icon: "💹",
      fields: DB.PL_FIELDS, leftPrefix: "TO_", rightPrefix: "BY_",
      leftHead: "Dr. (To)", rightHead: "Cr. (By)", firmOnly: true },
    balance: { table: "BALANCE_SHEET", title: "Balance Sheet", icon: "⚖️",
      fields: DB.BALANCE_FIELDS, firmOnly: true,
      left: ["BILLS_PAYABLE","SUNDRY_CREDITORS","LOANS","OUTSTANDING_EXPENSES","CAPITAL","NET_PROFIT","INTEREST_ON_CAPITAL","DRAWINGS","NET_LOSS","INCOME_TAX"],
      right: ["CASH_IN_HAND","CASH_AT_BANK","INVESTMENTS","BILLS_RECEIVABLE","SUNDRY_DEBTORS","CLOSING_STOCK","STORES","PLANT_AND_MACHINERY","FREEHOLD_PREMISES","UNEXPIRED_EXPENSES","GOODWILL"],
      leftHead: "Liabilities & Capital", rightHead: "Assets" }
  };

  function viewLedger(view, kind) {
    const cfg = LEDGERS[kind];
    setCrumbs(cfg.title, "Firm accounts module"); markNav(kind);
    const firms = DB.all("CLIENT_RECORD").filter(c => Number(c.INDV_HUF_FIRM_AOP_LA) === 2);
    const render = () => {
      const rows = DB.all(cfg.table);
      $("#lBody").innerHTML = rows.length ? rows.map(r => { const c = DB.findClient(r.PAN);
        const t = ledgerTotals(cfg, r);
        return `<tr><td class="mono">${esc(r.PAN)}</td><td><b>${esc(c?c.CLIENT_NAME:"—")}</b></td>
          <td>${esc(fyLabel({ASSES_YEAR_1:r.ASSES_YEAR_1,ASSES_YEAR_2:r.ASSES_YEAR_2}))}</td>
          <td class="num mono">${inr(t.left)}</td><td class="num mono">${inr(t.right)}</td>
          <td>${t.balanced?'<span class="badge badge-firm">Balanced</span>':'<span class="badge badge-revised">Δ '+inr(Math.abs(t.left-t.right))+'</span>'}</td>
          <td class="no-print"><div class="row-actions">
            <button class="btn btn-sm btn-ghost" data-edit="${esc(DB.acctKey(r))}">Edit</button>
            <button class="btn btn-sm btn-danger" data-del="${esc(DB.acctKey(r))}">Delete</button></div></td></tr>`; }).join("")
        : `<tr><td colspan="7"><div class="empty"><div class="big">${cfg.icon}</div>No ${esc(cfg.title.toLowerCase())} records yet.</div></td></tr>`;
      $$("#lBody [data-del]").forEach(b => b.onclick = () => { const rec = DB.all(cfg.table).find(x => DB.acctKey(x)===b.getAttribute("data-del"));
        confirmModal("Delete record?", `Delete the ${esc(cfg.title.toLowerCase())} for ${esc(rec.PAN)}?`, "Delete",
          () => { DB.deleteAcct(cfg.table, rec); toast("Record deleted"); render(); }, true); });
      $$("#lBody [data-edit]").forEach(b => b.onclick = () => openLedgerForm(cfg, kind, DB.all(cfg.table).find(x => DB.acctKey(x)===b.getAttribute("data-edit"))));
    };
    view.innerHTML = `
      <div class="page-head"><div><h2>${esc(cfg.title)}</h2>
        <p class="muted">${kind==="balance"?"Maintain assets, liabilities & capital for firm clients.":"Record the "+esc(cfg.title.toLowerCase())+" for firm clients; both sides are auto-totalled."}</p></div>
        <button class="btn btn-primary no-print" id="newL" ${firms.length?"":"disabled title='Add a firm client first'"}>+ New ${esc(cfg.title)}</button></div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr>
        <th>PAN</th><th>Firm</th><th>AY</th><th class="num">${esc(cfg.leftHead)}</th><th class="num">${esc(cfg.rightHead)}</th><th>Status</th><th class="no-print">Actions</th>
        </tr></thead><tbody id="lBody"></tbody></table></div></div>
      ${firms.length?"":`<p class="muted" style="margin-top:1rem">Only <b>Firm</b> category clients can have ${esc(cfg.title.toLowerCase())} records. Create a firm client first.</p>`}`;
    render();
    if (firms.length) $("#newL").onclick = () => openLedgerForm(cfg, kind, null);
    global.__ledgerRender = render;
  }

  function ledgerTotals(cfg, rec) {
    const sum = (keys) => keys.reduce((a,k)=>a+Number(rec[k]||0),0);
    let left, right;
    if (cfg.left) { left = sum(cfg.left); right = sum(cfg.right); }
    else { left = sum(cfg.fields.filter(f=>f.startsWith(cfg.leftPrefix))); right = sum(cfg.fields.filter(f=>f.startsWith(cfg.rightPrefix))); }
    return { left, right, balanced: Math.abs(left-right) < 1 };
  }

  function openLedgerForm(cfg, kind, existing) {
    const firms = DB.all("CLIENT_RECORD").filter(c => Number(c.INDV_HUF_FIRM_AOP_LA) === 2);
    let rec = existing ? Object.assign({}, existing) :
      (kind==="trading"?DB.mkTrading:kind==="pl"?DB.mkPL:DB.mkBalance)({ PAN: firms[0].PAN });
    const leftKeys = cfg.left || cfg.fields.filter(f=>f.startsWith(cfg.leftPrefix));
    const rightKeys = cfg.right || cfg.fields.filter(f=>f.startsWith(cfg.rightPrefix));
    const inputRows = (keys) => keys.map(k => `<div class="field" style="margin-bottom:.5rem">
      <label>${esc(humanize(k))}</label><input class="lcalc" data-k="${k}" type="number" min="0" step="1" value="${Number(rec[k])||""}" placeholder="0"></div>`).join("");

    const back = el(`<div class="modal-back"><div class="modal" style="width:min(920px,96vw)">
      <div class="m-head" style="display:flex;justify-content:space-between;align-items:center">
        <h3>${existing?"Edit":"New"} ${esc(cfg.title)}</h3><button class="icon-btn" data-x>✕</button></div>
      <div class="m-body" style="max-height:70vh;overflow:auto">
        <div class="form-grid" style="margin-bottom:.5rem">
          <div class="field"><label>Firm (PAN)</label><select id="lPAN" ${existing?"disabled":""}>
            ${firms.map(c=>`<option value="${esc(c.PAN)}" ${c.PAN===rec.PAN?"selected":""}>${esc(c.CLIENT_NAME)} — ${esc(c.PAN)}</option>`).join("")}</select></div>
          <div class="field"><label>AY From</label><input id="lAY1" type="date" value="${esc(rec.ASSES_YEAR_1)}" ${existing?"readonly":""}></div>
          <div class="field"><label>AY To</label><input id="lAY2" type="date" value="${esc(rec.ASSES_YEAR_2)}" ${existing?"readonly":""}></div>
        </div>
        <div class="ledger"><div class="side"><h4>${esc(cfg.leftHead)}</h4>${inputRows(leftKeys)}
            <div class="total"><span>Total</span><span id="lLeft" class="mono">₹0</span></div></div>
          <div class="side"><h4>${esc(cfg.rightHead)}</h4>${inputRows(rightKeys)}
            <div class="total"><span>Total</span><span id="lRight" class="mono">₹0</span></div></div></div>
        <div id="lStatus" style="text-align:center;margin-top:.8rem;font-weight:700"></div>
      </div>
      <div class="m-foot"><button class="btn btn-ghost" data-x>Cancel</button>
        <button class="btn btn-primary" data-save>💾 Save</button></div></div></div>`);
    document.body.appendChild(back);
    const close = () => back.remove();
    $$("[data-x]", back).forEach(b => b.onclick = close);
    back.addEventListener("click", e => { if (e.target === back) close(); });

    const read = () => { const o = Object.assign({}, rec);
      $$(".lcalc", back).forEach(i => o[i.getAttribute("data-k")] = Number(i.value)||0);
      o.PAN = $("#lPAN", back).value; o.ASSES_YEAR_1 = $("#lAY1", back).value; o.ASSES_YEAR_2 = $("#lAY2", back).value; return o; };
    const upd = () => { const o = read(); const t = ledgerTotals(cfg, o);
      $("#lLeft", back).textContent = inr(t.left); $("#lRight", back).textContent = inr(t.right);
      $("#lStatus", back).innerHTML = t.balanced ? '<span class="balanced">✓ Both sides balanced</span>'
        : `<span class="unbalanced">Difference of ${inr(Math.abs(t.left-t.right))} — ${cfg.title==="Balance Sheet"?"assets ≠ liabilities":"credit ≠ debit"}</span>`; };
    upd();
    $$(".lcalc", back).forEach(i => i.addEventListener("input", upd));

    $("[data-save]", back).onclick = () => {
      const o = read();
      if (!o.ASSES_YEAR_1 || !o.ASSES_YEAR_2) { toast("Assessment year required", "", "err"); return; }
      DB.upsertAcct(cfg.table, o);
      toast(cfg.title + " saved", DB.findClient(o.PAN)?.CLIENT_NAME);
      close(); if (global.__ledgerRender) global.__ledgerRender();
    };
  }

  /* =========================================================================
   * REPORTS
   * =======================================================================*/
  function viewReports(view) {
    setCrumbs("Reports", "Report Generation module"); markNav("reports");
    const clients = DB.all("CLIENT_RECORD"), returns = DB.all("INCOME_TAX_RECORD");
    const fiscals = Array.from(new Set(returns.map(fyLabel))).sort();
    view.innerHTML = `
      <div class="page-head"><div><h2>Report Generation</h2>
        <p class="muted">Generate the four statutory reports defined in the SRS. Use “Print” to save as PDF.</p></div></div>
      <div class="grid grid-2 no-print">
        <div class="card"><div class="card-head"><h3>1 · Return history of a client</h3></div>
          <div class="card-body"><div class="field"><label>Select client</label>
            <select id="r1"><option value="">— choose —</option>${clients.map(c=>`<option value="${esc(c.PAN)}">${esc(c.CLIENT_NAME)} (${esc(c.PAN)})</option>`).join("")}</select></div>
            <button class="btn btn-primary" data-run="1">Generate</button></div></div>
        <div class="card"><div class="card-head"><h3>2 · Return filed by a client in a fiscal</h3></div>
          <div class="card-body"><div class="form-grid">
            <div class="field"><label>Client</label><select id="r2c"><option value="">— choose —</option>${clients.map(c=>`<option value="${esc(c.PAN)}">${esc(c.CLIENT_NAME)}</option>`).join("")}</select></div>
            <div class="field"><label>Fiscal</label><select id="r2f">${fiscals.map(f=>`<option>${esc(f)}</option>`).join("")}</select></div></div>
            <button class="btn btn-primary" data-run="2">Generate</button></div></div>
        <div class="card"><div class="card-head"><h3>3 · Total returns filed in a fiscal</h3></div>
          <div class="card-body"><div class="field"><label>Fiscal</label>
            <select id="r3">${fiscals.map(f=>`<option>${esc(f)}</option>`).join("")}</select></div>
            <button class="btn btn-primary" data-run="3">Generate</button></div></div>
        <div class="card"><div class="card-head"><h3>4 · Total revised returns by a client</h3></div>
          <div class="card-body"><div class="field"><label>Client</label>
            <select id="r4"><option value="">— choose —</option>${clients.map(c=>`<option value="${esc(c.PAN)}">${esc(c.CLIENT_NAME)}</option>`).join("")}</select></div>
            <button class="btn btn-primary" data-run="4">Generate</button></div></div>
      </div>
      <div id="reportOut" style="margin-top:1.4rem"></div>`;

    $$("[data-run]").forEach(b => b.onclick = () => runReport(+b.getAttribute("data-run")));
  }

  function reportShell(title, rows, cols, subtitle) {
    const out = $("#reportOut");
    if (!rows.length) { out.innerHTML = `<div class="empty">No matching records for this selection.</div>`; return; }
    out.innerHTML = `<div class="btn-row no-print" style="justify-content:flex-end;margin-bottom:.6rem">
        <button class="btn btn-accent" onclick="window.print()">🖨️ Print / Save PDF</button></div>
      <div class="report-doc"><h1>${esc(title)}</h1>
      <div class="rmeta"><span>Income Tax Evaluation System</span><span>Generated: ${new Date().toLocaleString("en-GB")}</span></div>
      ${subtitle?`<p style="text-align:center;color:#555;margin-top:-.5rem">${esc(subtitle)}</p>`:""}
      <table><thead><tr>${cols.map(c=>`<th${c.num?' style="text-align:right"':''}>${esc(c.label)}</th>`).join("")}</tr></thead>
      <tbody>${rows.map(r=>`<tr>${cols.map(c=>`<td${c.num?' style="text-align:right;font-variant-numeric:tabular-nums"':''}>${c.num?inr(r[c.key]):esc(r[c.key])}</td>`).join("")}</tr>`).join("")}</tbody></table>
      </div>`;
    out.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function runReport(n) {
    const returns = DB.all("INCOME_TAX_RECORD");
    const nm = (pan) => { const c = DB.findClient(pan); return c ? c.CLIENT_NAME : pan; };
    if (n === 1) {
      const pan = $("#r1").value; if (!pan) return toast("Select a client", "", "warn");
      const rows = returns.filter(r => r.PAN === pan).map(r => ({ ay: fyLabel(r), type: Number(r.RETURN_ORIGINAL_REVISED)?"Revised":"Original",
        ti: r.TOTAL_INCOME, tax: r.NET_TAX_PAYABLE, bal: r.BAL_TAX_PAYABLE_REFUND }));
      reportShell("Return History — " + nm(pan), rows,
        [{label:"Assessment Year",key:"ay"},{label:"Type",key:"type"},{label:"Total Income",key:"ti",num:1},{label:"Net Tax",key:"tax",num:1},{label:"Balance",key:"bal",num:1}],
        "PAN: " + pan);
    } else if (n === 2) {
      const pan = $("#r2c").value, f = $("#r2f").value; if (!pan) return toast("Select a client", "", "warn");
      const rows = returns.filter(r => r.PAN === pan && fyLabel(r) === f).map(r => ({ type: Number(r.RETURN_ORIGINAL_REVISED)?"Revised":"Original",
        gti: r.GROSS_TOTAL_INCOME, ti: r.TOTAL_INCOME, tax: r.NET_TAX_PAYABLE }));
      reportShell(`Return filed in ${f} — ${nm(pan)}`, rows,
        [{label:"Type",key:"type"},{label:"Gross Total Income",key:"gti",num:1},{label:"Total Income",key:"ti",num:1},{label:"Net Tax",key:"tax",num:1}]);
    } else if (n === 3) {
      const f = $("#r3").value;
      const rows = returns.filter(r => fyLabel(r) === f).map(r => ({ pan: r.PAN, name: nm(r.PAN),
        type: Number(r.RETURN_ORIGINAL_REVISED)?"Revised":"Original", ti: r.TOTAL_INCOME, tax: r.NET_TAX_PAYABLE }));
      reportShell(`All Returns filed in ${f}`, rows,
        [{label:"PAN",key:"pan"},{label:"Client",key:"name"},{label:"Type",key:"type"},{label:"Total Income",key:"ti",num:1},{label:"Net Tax",key:"tax",num:1}],
        `${rows.length} return(s) · Net tax ${inr(rows.reduce((a,r)=>a+Number(r.tax||0),0))}`);
    } else if (n === 4) {
      const pan = $("#r4").value; if (!pan) return toast("Select a client", "", "warn");
      const rows = returns.filter(r => r.PAN === pan && Number(r.RETURN_ORIGINAL_REVISED) === 1).map(r => ({ ay: fyLabel(r),
        ti: r.TOTAL_INCOME, tax: r.NET_TAX_PAYABLE }));
      reportShell(`Revised Returns — ${nm(pan)}`, rows,
        [{label:"Assessment Year",key:"ay"},{label:"Revised Total Income",key:"ti",num:1},{label:"Revised Net Tax",key:"tax",num:1}],
        `Total revised returns: ${rows.length}`);
    }
  }

  /* =========================================================================
   * GUIDED TOUR
   * =======================================================================*/
  const TOUR = [
    { sel: '[data-nav="dashboard"]', title: "Dashboard", body: "Start here for a live overview — client counts, returns filed, revised returns and total tax recorded." },
    { sel: '[data-nav="clients"]', title: "Client Information", body: "The master module. Add, edit and delete clients. PAN is validated and used as the primary key across all records." },
    { sel: '[data-nav="returns"]', title: "Return Filing", body: "File Original or Revised returns. The tax is computed live on the right — slabs, rebate, surcharge and cess." },
    { sel: '[data-nav="trading"]', title: "Firm Accounts", body: "For Firm clients, maintain the Trading Account, Profit & Loss Account and Balance Sheet with automatic Dr/Cr balancing." },
    { sel: '[data-nav="reports"]', title: "Reports", body: "Generate the four statutory reports and print or save them as PDF for the client file." },
    { sel: '#themeBtn', title: "Light / Dark", body: "Toggle the theme anytime. Your data lives safely in this browser — nothing leaves your device." }
  ];
  function startTour() {
    let i = 0; const back = el(`<div class="tour-back"></div>`); document.body.appendChild(back);
    let pop;
    const show = () => {
      const step = TOUR[i]; const target = $(step.sel);
      $$(".tour-highlight").forEach(n => n.classList.remove("tour-highlight"));
      if (target) target.classList.add("tour-highlight");
      if (pop) pop.remove();
      pop = el(`<div class="tour-pop"><h4>${esc(step.title)}</h4><p>${esc(step.body)}</p>
        <div class="t-foot"><small class="muted">${i+1} / ${TOUR.length}</small>
        <div class="btn-row"><button class="btn btn-sm btn-ghost" data-skip>Skip</button>
        <button class="btn btn-sm btn-primary" data-next>${i===TOUR.length-1?"Done":"Next →"}</button></div></div></div>`);
      document.body.appendChild(pop);
      const r = target ? target.getBoundingClientRect() : { left: innerWidth/2-170, bottom: 90, top: 90, right: 0 };
      let left = Math.min(Math.max(12, r.right + 12), innerWidth - 360);
      let top = Math.min(r.top, innerHeight - 180);
      if (innerWidth < 820) { left = Math.max(12, innerWidth/2 - 170); top = Math.min(r.bottom + 10, innerHeight - 180); }
      pop.style.left = left + "px"; pop.style.top = Math.max(12, top) + "px";
      $("[data-next]", pop).onclick = () => { i++; if (i >= TOUR.length) return end(); show(); };
      $("[data-skip]", pop).onclick = end;
    };
    const end = () => { $$(".tour-highlight").forEach(n => n.classList.remove("tour-highlight")); if (pop) pop.remove(); back.remove(); };
    back.onclick = end; show();
  }

  /* =========================================================================
   * ROUTER
   * =======================================================================*/
  function route() {
    if (!DB.session()) { renderLogin(); return; }
    if (!$(".app")) renderShell();
    const view = $("#view"); if (!view) { renderShell(); return route(); }
    $("#sidebar")?.classList.remove("open");
    const h = (location.hash || "#/dashboard").replace(/^#\//, "");
    const parts = h.split("/");
    view.innerHTML = "";
    try {
      switch (parts[0]) {
        case "dashboard": return viewDashboard(view);
        case "clients":
          if (parts[1] === "new") return viewClientForm(view, "new");
          if (parts[1] === "edit") return viewClientForm(view, "edit", decodeURIComponent(parts[2] || ""));
          return viewClients(view);
        case "returns":
          if (parts[1] === "new") return viewReturnForm(view, "new");
          if (parts[1] === "edit") return viewReturnForm(view, "edit", decodeURIComponent(parts.slice(2).join("/")));
          return viewReturns(view);
        case "trading": return viewLedger(view, "trading");
        case "pl": return viewLedger(view, "pl");
        case "balance": return viewLedger(view, "balance");
        case "reports": return viewReports(view);
        default: location.hash = "#/dashboard";
      }
    } catch (err) {
      console.error(err);
      view.innerHTML = `<div class="empty"><div class="big">⚠️</div>Something went wrong rendering this page.<br>
        <small class="muted">${esc(err.message)}</small><div style="margin-top:1rem"><a class="btn btn-primary" href="#/dashboard">Back to dashboard</a></div></div>`;
    }
  }

  function boot() { if (!DB.session()) renderLogin(); else { renderShell(); route(); } }

  window.addEventListener("hashchange", route);
  window.addEventListener("DOMContentLoaded", boot);
  if (document.readyState !== "loading") boot();

  // expose a tiny console helper for demos
  global.TaxSystem = { reset: () => { DB.resetDemo(); location.reload(); } };
})(window);
