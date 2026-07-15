/* =============================================================================
 * ITEMS · Income Tax Evaluation & Maintenance System
 * db.js — Client-side data layer (mirrors the Oracle schema from project.pdf)
 *
 * This module emulates the 5 Oracle tables described in the SRS
 * (CLIENT_RECORD, INCOME_TAX_RECORD, TRADING_ACCOUNT, PL_ACCOUNT,
 * BALANCE_SHEET) using browser localStorage so the demo runs fully offline
 * on GitHub Pages. The production build (see /src) uses the identical schema
 * on Oracle via ODP.NET.
 * ===========================================================================*/
(function (global) {
  "use strict";

  const STORE_KEY = "items_db_v1";
  const SESSION_KEY = "items_session_v1";

  /* ---- Reference / lookup values (match PDF radio-button semantics) ------- */
  const CATEGORY = ["Individual", "HUF", "Firm", "AOP", "Local Authority"];
  const RESIDENCE = ["Resident", "Non Resident", "Not Ordinarily Resident"];
  const SEX = ["Female", "Male"]; // index 1 = Male, matches PDF boolean
  const WARD = ["Ward", "Circle", "Special Range"];
  const RETURN_TYPE = ["Original", "Revised"];

  /* ---- Demo credentials (documented in README) ---------------------------- */
  const USERS = [
    { username: "admin", password: "admin@123", name: "System Administrator", role: "Administrator" },
    { username: "operator", password: "items@2025", name: "Data Entry Operator", role: "Operator" }
  ];

  /* ---- Seed data ---------------------------------------------------------- *
   * Clients + AY 2007-08 figures are taken verbatim from the Crystal Report
   * screenshots in project.pdf (pages 184-186). Two firms are added so the
   * Trading / P&L / Balance-Sheet modules have realistic content, plus a
   * current-year (AY 2024-25) return so the app feels live.
   * ------------------------------------------------------------------------- */
  function seed() {
    const clients = [
      mkClient({ PAN: "ABCPP1234D", CLIENT_NAME: "Digamber Prasad", FATHERS_NAME: "Sri Nageshwar Lal",
        DOB: "1984-10-10", ADDRESS: "12, Rajendra Nagar, New Delhi", PINCODE: "110003",
        TELEPHONE: "09891141538", SEX: 1, INDV_HUF_FIRM_AOP_LA: 0, RESIDENT_NR_NOR: 0, WARD: "Ward-24(3)" }),
      mkClient({ PAN: "AAKPV5521R", CLIENT_NAME: "Ravi Verma", FATHERS_NAME: "Sri Mohan Verma",
        DOB: "1970-12-01", ADDRESS: "88, Civil Lines, Kanpur", PINCODE: "208001",
        TELEPHONE: "09415012233", SEX: 1, INDV_HUF_FIRM_AOP_LA: 0, RESIDENT_NR_NOR: 0, WARD: "Circle-3" }),
      mkClient({ PAN: "AFZPR7788K", CLIENT_NAME: "Anish Ranjan", FATHERS_NAME: "Sri Vijay Ranjan",
        DOB: "1985-03-23", ADDRESS: "5B, Boring Road, Patna", PINCODE: "800001",
        TELEPHONE: "09334455667", SEX: 1, INDV_HUF_FIRM_AOP_LA: 0, RESIDENT_NR_NOR: 0, WARD: "Ward-6(1)" }),
      mkClient({ PAN: "AABFA9090J", CLIENT_NAME: "Anuranjan Traders", FATHERS_NAME: "—",
        DOB: "1980-01-01", ADDRESS: "Plot 41, Industrial Area, Ghaziabad", PINCODE: "201001",
        TELEPHONE: "01204567890", SEX: 1, INDV_HUF_FIRM_AOP_LA: 2, RESIDENT_NR_NOR: 0, WARD: "Special Range" }),
      mkClient({ PAN: "AADFS1212Q", CLIENT_NAME: "Sunrise Textiles", FATHERS_NAME: "—",
        DOB: "1992-06-15", ADDRESS: "Unit 7, MIDC, Bhiwandi, Maharashtra", PINCODE: "421302",
        TELEPHONE: "02522334455", SEX: 1, INDV_HUF_FIRM_AOP_LA: 2, RESIDENT_NR_NOR: 0, WARD: "Circle-9" })
    ];

    const returns = [
      mkReturn({ PAN: "ABCPP1234D", AY1: "2007-04-01", AY2: "2008-03-31", RETURN_ORIGINAL_REVISED: 0,
        INCOME_FROM_SALARY: 210000, TOTAL_INCOME: 200000, NET_TAX_PAYABLE: 5000, TAX_DEDUC_AT_SOURCE: 4000 }),
      mkReturn({ PAN: "AAKPV5521R", AY1: "2007-04-01", AY2: "2008-03-31", RETURN_ORIGINAL_REVISED: 0,
        INCOME_FROM_SALARY: 315000, TOTAL_INCOME: 300000, NET_TAX_PAYABLE: 15000, TAX_DEDUC_AT_SOURCE: 10000 }),
      mkReturn({ PAN: "AFZPR7788K", AY1: "2007-04-01", AY2: "2008-03-31", RETURN_ORIGINAL_REVISED: 0,
        INCOME_FROM_BUSINESS: 360000, TOTAL_INCOME: 350000, NET_TAX_PAYABLE: 21000, ADVANCE_TAX_PAID: 15000 }),
      mkReturn({ PAN: "AFZPR7788K", AY1: "2007-04-01", AY2: "2008-03-31", RETURN_ORIGINAL_REVISED: 1,
        INCOME_FROM_BUSINESS: 372000, TOTAL_INCOME: 362000, NET_TAX_PAYABLE: 23400, ADVANCE_TAX_PAID: 15000 }),
      mkReturn({ PAN: "AABFA9090J", AY1: "2007-04-01", AY2: "2008-03-31", RETURN_ORIGINAL_REVISED: 0,
        INCOME_FROM_BUSINESS: 260000, TOTAL_INCOME: 250000, NET_TAX_PAYABLE: 12000, ADVANCE_TAX_PAID: 8000 }),
      /* Current-year returns so reports have recent fiscals too */
      mkReturn({ PAN: "ABCPP1234D", AY1: "2024-04-01", AY2: "2025-03-31", RETURN_ORIGINAL_REVISED: 0,
        INCOME_FROM_SALARY: 1180000, INCOME_FROM_HOUSE_PROPERTY: 120000, TOTAL_INCOME: 1150000,
        LESS_DEDUCTION_UNDER_VIA: 150000, TAX_DEDUC_AT_SOURCE: 120000 }),
      mkReturn({ PAN: "AADFS1212Q", AY1: "2024-04-01", AY2: "2025-03-31", RETURN_ORIGINAL_REVISED: 0,
        INCOME_FROM_BUSINESS: 2450000, TOTAL_INCOME: 2450000, ADVANCE_TAX_PAID: 600000 }),
      mkReturn({ PAN: "AAKPV5521R", AY1: "2024-04-01", AY2: "2025-03-31", RETURN_ORIGINAL_REVISED: 0,
        INCOME_FROM_SALARY: 640000, TOTAL_INCOME: 640000, TAX_DEDUC_AT_SOURCE: 25000 })
    ];

    // Recompute tax for the current-year returns using the engine.
    returns.forEach(r => {
      if (r.ASSES_YEAR_1 >= "2024-01-01" && global.ITEMS_TAX) {
        Object.assign(r, global.ITEMS_TAX.compute(r));
      }
    });

    const trading = [
      mkTrading({ PAN: "AABFA9090J", AY1: "2007-04-01", AY2: "2008-03-31",
        TO_OPENING_STOCK: 120000, TO_PURCHASES: 860000, TO_WAGES: 145000, TO_CARRIAGE: 22000,
        TO_GROSS_PROFIT: 383000, BY_SALES: 1350000, BY_CLOSING_STOCK: 180000 }),
      mkTrading({ PAN: "AADFS1212Q", AY1: "2024-04-01", AY2: "2025-03-31",
        TO_OPENING_STOCK: 540000, TO_PURCHASES: 6200000, TO_WAGES: 820000, TO_COAL_WATER_GAS: 96000,
        TO_GROSS_PROFIT: 3244000, BY_SALES: 10200000, BY_CLOSING_STOCK: 700000 })
    ];

    const pl = [
      mkPL({ PAN: "AABFA9090J", AY1: "2007-04-01", AY2: "2008-03-31",
        TO_SALARIES_WAGES: 96000, TO_OFFICE_GODOWN_RENT: 48000, TO_INSURANCE: 14000,
        TO_DEPRECIATION: 35000, TO_NET_PROFIT: 210000, BY_GROSS_PROFIT: 383000, BY_INTEREST_RECEIVED: 20000 }),
      mkPL({ PAN: "AADFS1212Q", AY1: "2024-04-01", AY2: "2025-03-31",
        TO_SALARIES_WAGES: 640000, TO_OFFICE_GODOWN_RENT: 240000, TO_ADVERTISEMENT: 180000,
        TO_DEPRECIATION: 210000, TO_NET_PROFIT: 2100000, BY_GROSS_PROFIT: 3244000, BY_RENT_RECEIVED: 126000 })
    ];

    const balance = [
      mkBalance({ PAN: "AABFA9090J", AY1: "2007-04-01", AY2: "2008-03-31",
        CAPITAL: 800000, SUNDRY_CREDITORS: 210000, LOANS: 150000, NET_PROFIT: 210000,
        CASH_IN_HAND: 45000, CASH_AT_BANK: 260000, INVESTMENTS: 210000, SUNDRY_DEBTORS: 320000,
        CLOSING_STOCK: 180000, PLANT_AND_MACHINERY: 355000 }),
      mkBalance({ PAN: "AADFS1212Q", AY1: "2024-04-01", AY2: "2025-03-31",
        CAPITAL: 5200000, SUNDRY_CREDITORS: 1400000, LOANS: 900000, NET_PROFIT: 2100000,
        CASH_IN_HAND: 180000, CASH_AT_BANK: 2100000, INVESTMENTS: 800000, SUNDRY_DEBTORS: 2600000,
        CLOSING_STOCK: 700000, PLANT_AND_MACHINERY: 3220000 })
    ];

    return {
      CLIENT_RECORD: clients,
      INCOME_TAX_RECORD: returns,
      TRADING_ACCOUNT: trading,
      PL_ACCOUNT: pl,
      BALANCE_SHEET: balance,
      _meta: { seededAt: new Date().toISOString(), version: 1 }
    };
  }

  /* ---- Record factories (default every numeric column to 0) --------------- */
  function mkClient(o) {
    return Object.assign({
      PAN: "", CLIENT_NAME: "", FATHERS_NAME: "", DOB: "", ADDRESS: "", PINCODE: "",
      TELEPHONE: "", SEX: 1, INDV_HUF_FIRM_AOP_LA: 0, RESIDENT_NR_NOR: 0,
      WARD_CIRCLE_SPECIAL_RANGE: o.WARD || "Ward"
    }, stripWard(o));
  }
  function stripWard(o) { const c = Object.assign({}, o); delete c.WARD; return c; }

  const RETURN_NUM_FIELDS = [
    "INCOME_FOR_PREV_YEAR", "INCOME_FROM_SALARY", "INCOME_FROM_HOUSE_PROPERTY", "INCOME_FROM_BUSINESS",
    "TOTAL_SHORT_TERM_GAIN", "TOTAL_LONG_TERM_GAIN", "TOTAL_CAPITAL_GAINS", "INCOME_FROM_OTHER_SOURCES",
    "INCM_OTHER_PERS_TO_ADDED", "GROSS_TOTAL_INCOME", "LESS_DEDUCTION_UNDER_VIA", "TOTAL_INCOME",
    "AGRICULTURAL_INCOME", "INCOME_TO_BE_EXEMPTED", "INCOME_AT_NORM_RATE", "INCOME_TAX_NORM_RATE",
    "INCOME_AT_SPCL_RATE", "INCOME_TAX_SPCL_RATE", "TAX_ON_TOTAL_INCOME", "LESS_REBATE", "TAX_PAYABLE",
    "ADDITIONAL_SURCHARGE", "TOTAL_TAX_PAYABLE", "LESS_RELIEF", "NET_TAX_PAYABLE", "TAX_DEDUC_AT_SOURCE",
    "ADVANCE_TAX_PAID", "INTEREST_PAYABLE", "TOT_SELF_ASSESS_TAX_PAID", "BAL_TAX_PAYABLE_REFUND"
  ];
  function mkReturn(o) {
    const base = { PAN: "", ASSES_YEAR_1: o.AY1 || "", ASSES_YEAR_2: o.AY2 || "", RETURN_ORIGINAL_REVISED: 0 };
    RETURN_NUM_FIELDS.forEach(f => base[f] = 0);
    const c = Object.assign(base, o);
    delete c.AY1; delete c.AY2;
    return c;
  }

  function mkTrading(o) { return mkAcct(o, TRADING_FIELDS); }
  function mkPL(o) { return mkAcct(o, PL_FIELDS); }
  function mkBalance(o) { return mkAcct(o, BALANCE_FIELDS); }
  function mkAcct(o, fields) {
    const base = { PAN: "", ASSES_YEAR_1: o.AY1 || "", ASSES_YEAR_2: o.AY2 || "" };
    fields.forEach(f => base[f] = 0);
    const c = Object.assign(base, o);
    delete c.AY1; delete c.AY2;
    return c;
  }

  const TRADING_FIELDS = ["TO_OPENING_STOCK","TO_STOCK","TO_PURCHASES","TO_CARRIAGE","TO_OCTROI",
    "TO_IMPORT_DUTY_CUSTOMS","TO_WAGES","TO_COAL_WATER_GAS","TO_HEATING_LIGHTING_POWER",
    "TO_MANU_ASSEM_EXPEN","TO_CONSUMABLE_STORES","TO_DRCT_FACT_PROD_EXP","TO_ROYALTY","TO_GROSS_PROFIT",
    "BY_SALES","BY_CLOSING_STOCK","BY_STOCK","BY_GROSS_LOSS"];
  const PL_FIELDS = ["TO_GROSS_LOSS","TO_SALARIES_WAGES","TO_OFFICE_GODOWN_RENT","TO_OFFICE_EXPENSES",
    "TO_MISC_SUNDRY_EXPENSE","TO_INSURANCE","TO_STATION_PRINT","TO_STAFF_WELF_EXPENSE","TO_LIGHT_WATER_ELECT",
    "TO_ESTAB_EXPENSE","TO_POST_TLGRM_FAX_COUR_PH","TO_LAW_CHARGES","TO_REPAIRS","TO_DISTRIBUTION_EXPENSES",
    "TO_TRAVEL_EXPENSE","TO_GENERAL_EXPENSES","TO_STABLE_EXPENSES","TO_SELLING_EXPENSES","TO_CARRIAGE_OUTWARD",
    "TO_CARRIAGE_ON_SALES","TO_INDIRECT_WAGES","TO_AUDIT_FEES","TO_ENTERTAIN_EXPENSES","TO_INTEREST_PAID",
    "TO_DISCOUNT_ALLOWED","TO_BAD_DEBTS","TO_RESERVE_FOR_BAD_DEBTS","TO_DEPRECIATION","TO_INTEREST_ON_CAPITAL",
    "TO_DISCOUNTING_CHARGES","TO_BANK_CHARGES","TO_EXPORT_CHARGES","TO_TRADE_EXPENSES","TO_ADMIN_EXPENSES",
    "TO_FINANCIAL_EXPENSES","TO_COMMISSION_PAID","TO_ADVERTISEMENT","TO_CHARITY","TO_SAMPLE_EXPENSES",
    "TO_LICENCE_FEE","TO_DELIVERY_CHARGES","TO_BROKERAGE","TO_SALES_TAX","TO_LOSS_ON_SALE_OF_ASSET",
    "TO_LOSS_BY_THEFT_ACCIDENT","TO_NET_PROFIT","BY_GROSS_PROFIT","BY_INTEREST_RECEIVED","BY_RENT_RECEIVED",
    "BY_DISCOUNT_RECEIVED","BY_DIVIDENDS_RECEIVED","BY_PROF_FROM_SALE_OF_ASSET","BY_REFUND_OF_TAX",
    "BY_COMPENSAT_RECEIVED","BY_APPRENTICESHIP_PREMIUM","BY_DIFFER_IN_EXCHANGE","BY_INTEREST_ON_DRAWINGS",
    "BY_DISCOUNT_ON_CREDITORS","BY_BAD_DEBTS_RECOVERED","BY_MISC_RECEIPTS","BY_INC_IN_VALUE_OF_ASSET",
    "BY_INCOME_FROM_INVESTMENT","BY_RES_FOR_BAD_DOUBTS","BY_NET_LOSS"];
  const BALANCE_FIELDS = ["BILLS_PAYABLE","SUNDRY_CREDITORS","LOANS","OUTSTANDING_EXPENSES","CAPITAL",
    "NET_PROFIT","INTEREST_ON_CAPITAL","DRAWINGS","NET_LOSS","INCOME_TAX","CASH_IN_HAND","CASH_AT_BANK",
    "INVESTMENTS","BILLS_RECEIVABLE","SUNDRY_DEBTORS","CLOSING_STOCK","STORES","PLANT_AND_MACHINERY",
    "FREEHOLD_PREMISES","UNEXPIRED_EXPENSES","GOODWILL"];

  /* ---- Persistence -------------------------------------------------------- */
  function load() {
    let raw = null;
    try { raw = JSON.parse(global.localStorage.getItem(STORE_KEY)); } catch (e) { raw = null; }
    if (!raw || !raw.CLIENT_RECORD) { raw = seed(); persist(raw); }
    return raw;
  }
  function persist(db) {
    try { global.localStorage.setItem(STORE_KEY, JSON.stringify(db)); } catch (e) {/* private mode */}
  }

  let _db = null;
  function db() { if (!_db) _db = load(); return _db; }

  /* ---- Generic table operations ------------------------------------------ */
  function all(table) { return db()[table].slice(); }

  function findClient(pan) { return db().CLIENT_RECORD.find(c => c.PAN === pan) || null; }

  function returnKey(r) { return [r.PAN, r.ASSES_YEAR_1, r.ASSES_YEAR_2, r.RETURN_ORIGINAL_REVISED].join("|"); }
  function acctKey(r) { return [r.PAN, r.ASSES_YEAR_1, r.ASSES_YEAR_2].join("|"); }

  function upsertClient(rec) {
    const arr = db().CLIENT_RECORD;
    const i = arr.findIndex(c => c.PAN === rec.PAN);
    if (i >= 0) arr[i] = rec; else arr.push(rec);
    persist(_db); return rec;
  }
  function deleteClient(pan) {
    const d = db();
    d.CLIENT_RECORD = d.CLIENT_RECORD.filter(c => c.PAN !== pan);
    // Cascade like the Oracle FK relationships in the SRS.
    d.INCOME_TAX_RECORD = d.INCOME_TAX_RECORD.filter(r => r.PAN !== pan);
    d.TRADING_ACCOUNT = d.TRADING_ACCOUNT.filter(r => r.PAN !== pan);
    d.PL_ACCOUNT = d.PL_ACCOUNT.filter(r => r.PAN !== pan);
    d.BALANCE_SHEET = d.BALANCE_SHEET.filter(r => r.PAN !== pan);
    persist(d);
  }

  function upsertReturn(rec) {
    const arr = db().INCOME_TAX_RECORD;
    const i = arr.findIndex(r => returnKey(r) === returnKey(rec));
    if (i >= 0) arr[i] = rec; else arr.push(rec);
    persist(_db); return rec;
  }
  function deleteReturn(rec) {
    const d = db();
    d.INCOME_TAX_RECORD = d.INCOME_TAX_RECORD.filter(r => returnKey(r) !== returnKey(rec));
    persist(d);
  }
  function hasOriginal(pan, ay1, ay2) {
    return db().INCOME_TAX_RECORD.some(r => r.PAN === pan && r.ASSES_YEAR_1 === ay1 &&
      r.ASSES_YEAR_2 === ay2 && Number(r.RETURN_ORIGINAL_REVISED) === 0);
  }

  function upsertAcct(table, rec) {
    const arr = db()[table];
    const i = arr.findIndex(r => acctKey(r) === acctKey(rec));
    if (i >= 0) arr[i] = rec; else arr.push(rec);
    persist(_db); return rec;
  }
  function deleteAcct(table, rec) {
    const d = db();
    d[table] = d[table].filter(r => acctKey(r) !== acctKey(rec));
    persist(d);
  }

  function resetDemo() { _db = seed(); persist(_db); return _db; }

  /* ---- Session ------------------------------------------------------------ */
  function login(username, password) {
    const u = USERS.find(x => x.username === username && x.password === password);
    if (!u) return null;
    const s = { username: u.username, name: u.name, role: u.role, at: Date.now() };
    global.sessionStorage.setItem(SESSION_KEY, JSON.stringify(s));
    return s;
  }
  function session() {
    try { return JSON.parse(global.sessionStorage.getItem(SESSION_KEY)); } catch (e) { return null; }
  }
  function logout() { global.sessionStorage.removeItem(SESSION_KEY); }

  global.ITEMS_DB = {
    CATEGORY, RESIDENCE, SEX, WARD, RETURN_TYPE, USERS,
    RETURN_NUM_FIELDS, TRADING_FIELDS, PL_FIELDS, BALANCE_FIELDS,
    all, findClient, upsertClient, deleteClient,
    upsertReturn, deleteReturn, hasOriginal, returnKey, acctKey,
    upsertAcct, deleteAcct, resetDemo,
    mkClient, mkReturn, mkTrading, mkPL, mkBalance,
    login, session, logout
  };
})(window);
