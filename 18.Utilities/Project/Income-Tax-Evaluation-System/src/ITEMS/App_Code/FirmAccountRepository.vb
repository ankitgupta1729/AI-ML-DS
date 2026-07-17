' =============================================================================
' Income Tax Evaluation System · FirmAccountRepository.vb — generic CRUD for the three firm-account
' tables (TRADING_ACCOUNT, PL_ACCOUNT, BALANCE_SHEET). One code path drives all
' three by describing each table's money columns and its two ledger sides.
' =============================================================================
Imports System.Collections.Generic
Imports System.Data
Imports System.Text
Imports ITEMS.Data
Imports Oracle.ManagedDataAccess.Client

Namespace Repositories

    Public Class FirmAccountSpec
        Public Property Table As String
        Public Property Title As String
        Public Property LeftHead As String
        Public Property RightHead As String
        Public Property LeftCols As String()      ' debit / liabilities
        Public Property RightCols As String()      ' credit / assets
        Public ReadOnly Property AllCols As String()
            Get
                Dim l As New List(Of String)(LeftCols)
                l.AddRange(RightCols)
                Return l.ToArray()
            End Get
        End Property
    End Class

    Public NotInheritable Class FirmAccountRepository

        Private Sub New()
        End Sub

        Public Shared Function GetSpec(moduleKey As String) As FirmAccountSpec
            Select Case moduleKey
                Case "trading"
                    Return New FirmAccountSpec With {.Table = "TRADING_ACCOUNT", .Title = "Trading Account",
                        .LeftHead = "Dr. (To)", .RightHead = "Cr. (By)",
                        .LeftCols = {"TO_OPENING_STOCK","TO_STOCK","TO_PURCHASES","TO_CARRIAGE","TO_OCTROI","TO_IMPORT_DUTY_CUSTOMS","TO_WAGES","TO_COAL_WATER_GAS","TO_HEATING_LIGHTING_POWER","TO_MANU_ASSEM_EXPEN","TO_CONSUMABLE_STORES","TO_DRCT_FACT_PROD_EXP","TO_ROYALTY","TO_GROSS_PROFIT"},
                        .RightCols = {"BY_SALES","BY_CLOSING_STOCK","BY_STOCK","BY_GROSS_LOSS"}}
                Case "pl"
                    Return New FirmAccountSpec With {.Table = "PL_ACCOUNT", .Title = "Profit & Loss Account",
                        .LeftHead = "Dr. (To)", .RightHead = "Cr. (By)",
                        .LeftCols = {"TO_GROSS_LOSS","TO_SALARIES_WAGES","TO_OFFICE_GODOWN_RENT","TO_OFFICE_EXPENSES","TO_MISC_SUNDRY_EXPENSE","TO_INSURANCE","TO_STATION_PRINT","TO_STAFF_WELF_EXPENSE","TO_LIGHT_WATER_ELECT","TO_ESTAB_EXPENSE","TO_POST_TLGRM_FAX_COUR_PH","TO_LAW_CHARGES","TO_REPAIRS","TO_DISTRIBUTION_EXPENSES","TO_TRAVEL_EXPENSE","TO_GENERAL_EXPENSES","TO_STABLE_EXPENSES","TO_SELLING_EXPENSES","TO_CARRIAGE_OUTWARD","TO_CARRIAGE_ON_SALES","TO_INDIRECT_WAGES","TO_AUDIT_FEES","TO_ENTERTAIN_EXPENSES","TO_INTEREST_PAID","TO_DISCOUNT_ALLOWED","TO_BAD_DEBTS","TO_RESERVE_FOR_BAD_DEBTS","TO_DEPRECIATION","TO_INTEREST_ON_CAPITAL","TO_DISCOUNTING_CHARGES","TO_BANK_CHARGES","TO_EXPORT_CHARGES","TO_TRADE_EXPENSES","TO_ADMIN_EXPENSES","TO_FINANCIAL_EXPENSES","TO_COMMISSION_PAID","TO_ADVERTISEMENT","TO_CHARITY","TO_SAMPLE_EXPENSES","TO_LICENCE_FEE","TO_DELIVERY_CHARGES","TO_BROKERAGE","TO_SALES_TAX","TO_LOSS_ON_SALE_OF_ASSET","TO_LOSS_BY_THEFT_ACCIDENT","TO_NET_PROFIT"},
                        .RightCols = {"BY_GROSS_PROFIT","BY_INTEREST_RECEIVED","BY_RENT_RECEIVED","BY_DISCOUNT_RECEIVED","BY_DIVIDENDS_RECEIVED","BY_PROF_FROM_SALE_OF_ASSET","BY_REFUND_OF_TAX","BY_COMPENSAT_RECEIVED","BY_APPRENTICESHIP_PREMIUM","BY_DIFFER_IN_EXCHANGE","BY_INTEREST_ON_DRAWINGS","BY_DISCOUNT_ON_CREDITORS","BY_BAD_DEBTS_RECOVERED","BY_MISC_RECEIPTS","BY_INC_IN_VALUE_OF_ASSET","BY_INCOME_FROM_INVESTMENT","BY_RES_FOR_BAD_DOUBTS","BY_NET_LOSS"}}
                Case Else ' balance
                    Return New FirmAccountSpec With {.Table = "BALANCE_SHEET", .Title = "Balance Sheet",
                        .LeftHead = "Liabilities & Capital", .RightHead = "Assets",
                        .LeftCols = {"BILLS_PAYABLE","SUNDRY_CREDITORS","LOANS","OUTSTANDING_EXPENSES","CAPITAL","NET_PROFIT","INTEREST_ON_CAPITAL","DRAWINGS","NET_LOSS","INCOME_TAX"},
                        .RightCols = {"CASH_IN_HAND","CASH_AT_BANK","INVESTMENTS","BILLS_RECEIVABLE","SUNDRY_DEBTORS","CLOSING_STOCK","STORES","PLANT_AND_MACHINERY","FREEHOLD_PREMISES","UNEXPIRED_EXPENSES","GOODWILL"}}
            End Select
        End Function

        Public Shared Function List(spec As FirmAccountSpec) As DataTable
            Return OracleDb.Query(
                "SELECT a.*, c.CLIENT_NAME FROM " & spec.Table & " a JOIN CLIENT_RECORD c ON c.PAN=a.PAN ORDER BY a.ASSES_YEAR_1 DESC")
        End Function

        Public Shared Function [Get](spec As FirmAccountSpec, pan As String, a1 As Date, a2 As Date) As DataRow
            Return OracleDb.QueryRow("SELECT * FROM " & spec.Table & " WHERE PAN=:p AND ASSES_YEAR_1=:a1 AND ASSES_YEAR_2=:a2",
                                     OracleDb.PStr("p", pan), OracleDb.PDate("a1", a1), OracleDb.PDate("a2", a2))
        End Function

        Public Shared Function SideTotal(row As DataRow, cols As String()) As Decimal
            Dim t As Decimal = 0
            For Each c In cols
                If row.Table.Columns.Contains(c) AndAlso Not IsDBNull(row(c)) Then t += Convert.ToDecimal(row(c))
            Next
            Return t
        End Function

        ''' <summary>Insert or update using a column→value map (all parameterised).</summary>
        Public Shared Sub Save(spec As FirmAccountSpec, pan As String, a1 As Date, a2 As Date,
                               values As Dictionary(Of String, Decimal), isNew As Boolean)
            Dim ps As New List(Of OracleParameter) From {
                OracleDb.PStr("p", pan), OracleDb.PDate("a1", a1), OracleDb.PDate("a2", a2)}
            For Each kv In values
                ps.Add(OracleDb.PNum(kv.Key, kv.Value))
            Next

            If isNew Then
                Dim cols = New StringBuilder("PAN,ASSES_YEAR_1,ASSES_YEAR_2")
                Dim binds = New StringBuilder(":p,:a1,:a2")
                For Each kv In values
                    cols.Append(",").Append(kv.Key)
                    binds.Append(",:").Append(kv.Key)
                Next
                OracleDb.Execute($"INSERT INTO {spec.Table} ({cols}) VALUES ({binds})", ps.ToArray())
            Else
                Dim sets = New StringBuilder()
                For Each kv In values
                    If sets.Length > 0 Then sets.Append(",")
                    sets.Append(kv.Key).Append("=:").Append(kv.Key)
                Next
                OracleDb.Execute($"UPDATE {spec.Table} SET {sets} WHERE PAN=:p AND ASSES_YEAR_1=:a1 AND ASSES_YEAR_2=:a2", ps.ToArray())
            End If
        End Sub

        Public Shared Sub Delete(spec As FirmAccountSpec, pan As String, a1 As Date, a2 As Date)
            OracleDb.Execute($"DELETE FROM {spec.Table} WHERE PAN=:p AND ASSES_YEAR_1=:a1 AND ASSES_YEAR_2=:a2",
                             OracleDb.PStr("p", pan), OracleDb.PDate("a1", a1), OracleDb.PDate("a2", a2))
        End Sub

    End Class

End Namespace
