' =============================================================================
' ITEMS · ReturnRepository.vb — CRUD for the Original/Revised Return module
' and the four statutory reports (Report Generation module).
' =============================================================================
Imports System.Collections.Generic
Imports System.Data
Imports ITEMS.Data
Imports ITEMS.Logic
Imports ITEMS.Models

Namespace Repositories

    Public NotInheritable Class ReturnRepository

        Private Sub New()
        End Sub

        Private Shared Function N(o As Object) As Decimal
            Return If(IsDBNull(o), 0D, Convert.ToDecimal(o))
        End Function

        Private Shared Function Map(r As DataRow) As ReturnRecord
            Return New ReturnRecord With {
                .Pan = Convert.ToString(r("PAN")),
                .AyFrom = Convert.ToDateTime(r("ASSES_YEAR_1")),
                .AyTo = Convert.ToDateTime(r("ASSES_YEAR_2")),
                .ReturnType = Convert.ToInt32(r("RETURN_ORIGINAL_REVISED")),
                .IncomeFromSalary = N(r("INCOME_FROM_SALARY")),
                .IncomeFromHouseProperty = N(r("INCOME_FROM_HOUSE_PROPERTY")),
                .IncomeFromBusiness = N(r("INCOME_FROM_BUSINESS")),
                .ShortTermGain = N(r("TOTAL_SHORT_TERM_GAIN")),
                .LongTermGain = N(r("TOTAL_LONG_TERM_GAIN")),
                .TotalCapitalGains = N(r("TOTAL_CAPITAL_GAINS")),
                .IncomeFromOtherSources = N(r("INCOME_FROM_OTHER_SOURCES")),
                .OtherPersonIncome = N(r("INCM_OTHER_PERS_TO_ADDED")),
                .DeductionUnderVIA = N(r("LESS_DEDUCTION_UNDER_VIA")),
                .TdsAtSource = N(r("TAX_DEDUC_AT_SOURCE")),
                .AdvanceTaxPaid = N(r("ADVANCE_TAX_PAID")),
                .SelfAssessmentPaid = N(r("TOT_SELF_ASSESS_TAX_PAID")),
                .InterestPayable = N(r("INTEREST_PAYABLE")),
                .Relief = N(r("LESS_RELIEF")),
                .GrossTotalIncome = N(r("GROSS_TOTAL_INCOME")),
                .TotalIncome = N(r("TOTAL_INCOME")),
                .NetTaxPayable = N(r("NET_TAX_PAYABLE")),
                .BalancePayableRefund = N(r("BAL_TAX_PAYABLE_REFUND"))
            }
        End Function

        Public Shared Function GetAll() As List(Of ReturnRecord)
            Dim dt = OracleDb.Query("SELECT * FROM INCOME_TAX_RECORD ORDER BY ASSES_YEAR_1 DESC, PAN")
            Dim list As New List(Of ReturnRecord)()
            For Each r As DataRow In dt.Rows : list.Add(Map(r)) : Next
            Return list
        End Function

        Public Shared Function [Get](pan As String, ayFrom As Date, ayTo As Date, retType As Integer) As ReturnRecord
            Dim r = OracleDb.QueryRow(
                "SELECT * FROM INCOME_TAX_RECORD WHERE PAN=:p AND ASSES_YEAR_1=:a1 AND ASSES_YEAR_2=:a2 AND RETURN_ORIGINAL_REVISED=:t",
                OracleDb.PStr("p", pan), OracleDb.PDate("a1", ayFrom), OracleDb.PDate("a2", ayTo), OracleDb.PNum("t", retType))
            Return If(r Is Nothing, Nothing, Map(r))
        End Function

        Public Shared Function HasOriginal(pan As String, ayFrom As Date, ayTo As Date) As Boolean
            Return Convert.ToInt32(OracleDb.Scalar(
                "SELECT COUNT(*) FROM INCOME_TAX_RECORD WHERE PAN=:p AND ASSES_YEAR_1=:a1 AND ASSES_YEAR_2=:a2 AND RETURN_ORIGINAL_REVISED=0",
                OracleDb.PStr("p", pan), OracleDb.PDate("a1", ayFrom), OracleDb.PDate("a2", ayTo))) > 0
        End Function

        ''' <summary>Insert or update a return; computes tax before persisting.</summary>
        Public Shared Sub Save(rec As ReturnRecord, isFirm As Boolean, isNew As Boolean)
            Dim t As TaxResult = TaxEngine.Compute(rec, isFirm)
            rec.GrossTotalIncome = t.GrossTotalIncome
            rec.TotalIncome = t.TotalIncome
            rec.NetTaxPayable = t.NetTaxPayable
            rec.BalancePayableRefund = t.BalancePayableOrRefund

            Dim ps() As Oracle.ManagedDataAccess.Client.OracleParameter = {
                OracleDb.PStr("p", rec.Pan), OracleDb.PDate("a1", rec.AyFrom), OracleDb.PDate("a2", rec.AyTo),
                OracleDb.PNum("t", rec.ReturnType), OracleDb.PNum("sal", rec.IncomeFromSalary),
                OracleDb.PNum("hp", rec.IncomeFromHouseProperty), OracleDb.PNum("bus", rec.IncomeFromBusiness),
                OracleDb.PNum("stg", rec.ShortTermGain), OracleDb.PNum("ltg", rec.LongTermGain),
                OracleDb.PNum("cg", rec.TotalCapitalGains), OracleDb.PNum("oth", rec.IncomeFromOtherSources),
                OracleDb.PNum("clb", rec.OtherPersonIncome), OracleDb.PNum("via", rec.DeductionUnderVIA),
                OracleDb.PNum("tds", rec.TdsAtSource), OracleDb.PNum("adv", rec.AdvanceTaxPaid),
                OracleDb.PNum("saj", rec.SelfAssessmentPaid), OracleDb.PNum("intr", rec.InterestPayable),
                OracleDb.PNum("rel", rec.Relief), OracleDb.PNum("gti", t.GrossTotalIncome),
                OracleDb.PNum("ti", t.TotalIncome), OracleDb.PNum("tont", t.TaxOnTotalIncome),
                OracleDb.PNum("reb", t.Rebate87A), OracleDb.PNum("sur", t.Surcharge),
                OracleDb.PNum("ttp", t.TotalTaxPayable), OracleDb.PNum("ntp", t.NetTaxPayable),
                OracleDb.PNum("bal", t.BalancePayableOrRefund)}

            If isNew Then
                OracleDb.Execute(
                    "INSERT INTO INCOME_TAX_RECORD (PAN,ASSES_YEAR_1,ASSES_YEAR_2,RETURN_ORIGINAL_REVISED," &
                    "INCOME_FROM_SALARY,INCOME_FROM_HOUSE_PROPERTY,INCOME_FROM_BUSINESS,TOTAL_SHORT_TERM_GAIN,TOTAL_LONG_TERM_GAIN," &
                    "TOTAL_CAPITAL_GAINS,INCOME_FROM_OTHER_SOURCES,INCM_OTHER_PERS_TO_ADDED,LESS_DEDUCTION_UNDER_VIA," &
                    "TAX_DEDUC_AT_SOURCE,ADVANCE_TAX_PAID,TOT_SELF_ASSESS_TAX_PAID,INTEREST_PAYABLE,LESS_RELIEF," &
                    "GROSS_TOTAL_INCOME,TOTAL_INCOME,TAX_ON_TOTAL_INCOME,LESS_REBATE,ADDITIONAL_SURCHARGE,TOTAL_TAX_PAYABLE,NET_TAX_PAYABLE,BAL_TAX_PAYABLE_REFUND) " &
                    "VALUES (:p,:a1,:a2,:t,:sal,:hp,:bus,:stg,:ltg,:cg,:oth,:clb,:via,:tds,:adv,:saj,:intr,:rel,:gti,:ti,:tont,:reb,:sur,:ttp,:ntp,:bal)", ps)
            Else
                OracleDb.Execute(
                    "UPDATE INCOME_TAX_RECORD SET INCOME_FROM_SALARY=:sal,INCOME_FROM_HOUSE_PROPERTY=:hp,INCOME_FROM_BUSINESS=:bus," &
                    "TOTAL_SHORT_TERM_GAIN=:stg,TOTAL_LONG_TERM_GAIN=:ltg,TOTAL_CAPITAL_GAINS=:cg,INCOME_FROM_OTHER_SOURCES=:oth," &
                    "INCM_OTHER_PERS_TO_ADDED=:clb,LESS_DEDUCTION_UNDER_VIA=:via,TAX_DEDUC_AT_SOURCE=:tds,ADVANCE_TAX_PAID=:adv," &
                    "TOT_SELF_ASSESS_TAX_PAID=:saj,INTEREST_PAYABLE=:intr,LESS_RELIEF=:rel,GROSS_TOTAL_INCOME=:gti,TOTAL_INCOME=:ti," &
                    "TAX_ON_TOTAL_INCOME=:tont,LESS_REBATE=:reb,ADDITIONAL_SURCHARGE=:sur,TOTAL_TAX_PAYABLE=:ttp,NET_TAX_PAYABLE=:ntp,BAL_TAX_PAYABLE_REFUND=:bal " &
                    "WHERE PAN=:p AND ASSES_YEAR_1=:a1 AND ASSES_YEAR_2=:a2 AND RETURN_ORIGINAL_REVISED=:t", ps)
            End If
        End Sub

        Public Shared Sub Delete(pan As String, ayFrom As Date, ayTo As Date, retType As Integer)
            OracleDb.Execute(
                "DELETE FROM INCOME_TAX_RECORD WHERE PAN=:p AND ASSES_YEAR_1=:a1 AND ASSES_YEAR_2=:a2 AND RETURN_ORIGINAL_REVISED=:t",
                OracleDb.PStr("p", pan), OracleDb.PDate("a1", ayFrom), OracleDb.PDate("a2", ayTo), OracleDb.PNum("t", retType))
        End Sub

        ' -- Reports (Report Generation module) ---------------------------------
        Public Shared Function ReturnHistory(pan As String) As DataTable
            Return OracleDb.Query("SELECT * FROM V_RETURN_HISTORY WHERE PAN = :p ORDER BY ASSESSMENT_YEAR, RETURN_TYPE",
                                  OracleDb.PStr("p", pan))
        End Function

        Public Shared Function ReturnsInFiscal(ayFrom As Date) As DataTable
            Return OracleDb.Query("SELECT * FROM V_RETURN_HISTORY WHERE ASSESSMENT_YEAR = :ay ORDER BY CLIENT_NAME",
                                  OracleDb.PStr("ay", ayFrom.ToString("yyyy") & "-" & ayFrom.AddYears(1).ToString("yy")))
        End Function

        Public Shared Function RevisedByClient(pan As String) As DataTable
            Return OracleDb.Query("SELECT * FROM V_RETURN_HISTORY WHERE PAN = :p AND RETURN_TYPE = 'Revised' ORDER BY ASSESSMENT_YEAR",
                                  OracleDb.PStr("p", pan))
        End Function

    End Class

End Namespace
