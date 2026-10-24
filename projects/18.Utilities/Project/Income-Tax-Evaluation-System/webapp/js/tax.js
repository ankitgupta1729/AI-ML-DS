/* =============================================================================
 * Income Tax Evaluation System · tax.js — computation engine
 *
 * Implements a self-consistent slab computation for the INCOME_TAX_RECORD
 * form fields described in project.pdf (Gross Total Income -> deductions ->
 * Total Income -> tax by slab -> rebate 87A -> surcharge -> health & education
 * cess -> less TDS/advance/self-assessment -> balance payable / refundable).
 *
 * Slabs follow the Indian "old regime" (AY 2024-25) for a resident individual.
 * Firms are taxed at a flat 30%. Values are illustrative for demonstration.
 * ===========================================================================*/
(function (global) {
  "use strict";

  const CESS_RATE = 0.04;            // Health & Education Cess
  const REBATE_87A_LIMIT = 500000;   // total income up to which rebate applies
  const REBATE_87A_MAX = 12500;
  const FIRM_RATE = 0.30;

  const SLABS = [
    { upto: 250000, rate: 0.00 },
    { upto: 500000, rate: 0.05 },
    { upto: 1000000, rate: 0.20 },
    { upto: Infinity, rate: 0.30 }
  ];

  // Surcharge on income-tax when total income crosses these thresholds.
  const SURCHARGE = [
    { over: 50000000, rate: 0.37 },
    { over: 20000000, rate: 0.25 },
    { over: 10000000, rate: 0.15 },
    { over: 5000000, rate: 0.10 },
    { over: 0, rate: 0.00 }
  ];

  function n(v) { const x = Number(v); return isFinite(x) ? x : 0; }

  function slabTax(income) {
    let tax = 0, lower = 0;
    for (const s of SLABS) {
      if (income > lower) {
        const band = Math.min(income, s.upto) - lower;
        tax += band * s.rate;
        lower = s.upto;
      } else break;
    }
    return Math.round(tax);
  }

  function surchargeRate(totalIncome) {
    for (const s of SURCHARGE) if (totalIncome > s.over) return s.rate;
    return 0;
  }

  /**
   * compute(rec) — given an INCOME_TAX_RECORD (partial), returns the derived
   * computation fields. Non-destructive: returns only the computed keys.
   * @param {object} rec  return record with income + payment fields
   * @param {object} client  optional CLIENT_RECORD (to detect firm category)
   */
  function compute(rec, client) {
    const salary = n(rec.INCOME_FROM_SALARY);
    const house = n(rec.INCOME_FROM_HOUSE_PROPERTY);
    const business = n(rec.INCOME_FROM_BUSINESS);
    const stcg = n(rec.TOTAL_SHORT_TERM_GAIN);
    const ltcg = n(rec.TOTAL_LONG_TERM_GAIN);
    const capital = n(rec.TOTAL_CAPITAL_GAINS) || (stcg + ltcg);
    const other = n(rec.INCOME_FROM_OTHER_SOURCES);
    const clubbed = n(rec.INCM_OTHER_PERS_TO_ADDED);

    const gross = salary + house + business + capital + other + clubbed;
    const deductions = Math.min(n(rec.LESS_DEDUCTION_UNDER_VIA), gross);
    const totalIncome = Math.max(0, gross - deductions);

    const isFirm = client && Number(client.INDV_HUF_FIRM_AOP_LA) === 2;

    // Special-rate income (LTCG @ 20% here for illustration); rest at normal.
    const spclBase = ltcg;
    const normalBase = Math.max(0, totalIncome - spclBase);

    const taxNormal = isFirm ? Math.round(totalIncome * FIRM_RATE) : slabTax(normalBase);
    const taxSpecial = isFirm ? 0 : Math.round(spclBase * 0.20);
    const taxOnTotal = taxNormal + taxSpecial;

    let rebate = 0;
    if (!isFirm && totalIncome <= REBATE_87A_LIMIT) rebate = Math.min(taxOnTotal, REBATE_87A_MAX);

    const taxPayable = Math.max(0, taxOnTotal - rebate);
    const surcharge = Math.round(taxPayable * surchargeRate(totalIncome));
    const cess = Math.round((taxPayable + surcharge) * CESS_RATE);
    const totalTaxPayable = taxPayable + surcharge + cess;

    const relief = n(rec.LESS_RELIEF);
    const tds = n(rec.TAX_DEDUC_AT_SOURCE);
    const advance = n(rec.ADVANCE_TAX_PAID);
    const selfAssess = n(rec.TOT_SELF_ASSESS_TAX_PAID);
    const interest = n(rec.INTEREST_PAYABLE);

    const netTaxPayable = Math.max(0, totalTaxPayable - relief);
    const balance = netTaxPayable + interest - tds - advance - selfAssess;

    return {
      GROSS_TOTAL_INCOME: gross,
      TOTAL_INCOME: totalIncome,
      INCOME_AT_NORM_RATE: normalBase,
      INCOME_TAX_NORM_RATE: taxNormal,
      INCOME_AT_SPCL_RATE: spclBase,
      INCOME_TAX_SPCL_RATE: taxSpecial,
      TAX_ON_TOTAL_INCOME: taxOnTotal,
      LESS_REBATE: rebate,
      TAX_PAYABLE: taxPayable,
      ADDITIONAL_SURCHARGE: surcharge,
      TOTAL_TAX_PAYABLE: totalTaxPayable,
      NET_TAX_PAYABLE: netTaxPayable,
      BAL_TAX_PAYABLE_REFUND: Math.round(balance)
    };
  }

  global.TaxEngine = { compute, slabTax, SLABS };
})(window);
