Imports Oracle.ManagedDataAccess.Client
Imports System.Collections.Generic
Imports System.Configuration

Namespace Data

    Public Class OracleDataAccess
        Private Shared _connectionString As String

        Shared Sub New()
            _connectionString = ConfigurationManager.ConnectionStrings("IncomeTaxDB").ConnectionString
        End Sub

        Private Shared Function GetConnection() As OracleConnection
            Return New OracleConnection(_connectionString)
        End Function

        Public Shared Function ExecuteQuery(query As String, Optional params As OracleParameter() = Nothing) As DataTable
            Dim dt As New DataTable()
            Using conn As OracleConnection = GetConnection()
                Using cmd As New OracleCommand(query, conn)
                    cmd.BindByName = True
                    If params IsNot Nothing Then cmd.Parameters.AddRange(params)
                    Using adapter As New OracleDataAdapter(cmd)
                        adapter.Fill(dt)
                    End Using
                End Using
            End Using
            Return dt
        End Function

        Public Shared Function ExecuteNonQuery(query As String, Optional params As OracleParameter() = Nothing) As Integer
            Using conn As OracleConnection = GetConnection()
                Using cmd As New OracleCommand(query, conn)
                    cmd.BindByName = True
                    If params IsNot Nothing Then cmd.Parameters.AddRange(params)
                    conn.Open()
                    Return cmd.ExecuteNonQuery()
                End Using
            End Using
        End Function

        Public Shared Function ExecuteScalar(query As String, Optional params As OracleParameter() = Nothing) As Object
            Using conn As OracleConnection = GetConnection()
                Using cmd As New OracleCommand(query, conn)
                    cmd.BindByName = True
                    If params IsNot Nothing Then cmd.Parameters.AddRange(params)
                    conn.Open()
                    Return cmd.ExecuteScalar()
                End Using
            End Using
        End Function

        Public Shared Function ValidateUser(userId As String, password As String) As DataTable
            Dim sql = "SELECT * FROM APP_USERS WHERE USER_ID = :uid AND PASSWORD_HASH = :pwd AND IS_ACTIVE = 'Y'"
            Dim p() As OracleParameter = {
                New OracleParameter(":uid", userId),
                New OracleParameter(":pwd", password)
            }
            Return ExecuteQuery(sql, p)
        End Function

        Public Shared Function GetAllClients(Optional search As String = "") As DataTable
            Dim sql As String = "SELECT * FROM CLIENT_RECORD"
            Dim params As New List(Of OracleParameter)()
            If Not String.IsNullOrEmpty(search) Then
                sql &= " WHERE CLIENT_CODE LIKE :search OR FULL_NAME LIKE :search OR PAN LIKE :search"
                params.Add(New OracleParameter(":search", "%" & search & "%"))
            End If
            sql &= " ORDER BY UPDATED_DATE DESC"
            Return ExecuteQuery(sql, If(params.Count > 0, params.ToArray(), Nothing))
        End Function

        Public Shared Function GetClientByCode(clientCode As String) As DataTable
            Dim sql = "SELECT * FROM CLIENT_RECORD WHERE CLIENT_CODE = :code"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode)}
            Return ExecuteQuery(sql, p)
        End Function

        Public Shared Function InsertUpdateClient(record As Models.ClientRecord) As Integer
            Dim checkSql = "SELECT COUNT(*) FROM CLIENT_RECORD WHERE CLIENT_CODE = :code"
            Dim count = Convert.ToInt32(ExecuteScalar(checkSql, New OracleParameter(":code", record.ClientCode)))
            If count > 0 Then
                Dim sql = "UPDATE CLIENT_RECORD SET FULL_NAME=:name, PAN=:pan, DATE_OF_BIRTH=:dob, GENDER=:gender, ADDRESS=:addr, CITY=:city, STATE=:state, PINCODE=:pin, TELEPHONE=:tel, MOBILE=:mob, EMAIL=:email, OCCUPATION=:occ, AADHAR_NUMBER=:aadhar, WARD_CIRCLE_SPECIAL_RANGE=:ward, ASSESSMENT_YEAR=:year, UPDATED_DATE=SYSDATE, UPDATED_BY=:updatedBy WHERE CLIENT_CODE=:code"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode),
                    New OracleParameter(":name", record.FullName), New OracleParameter(":pan", record.PAN),
                    New OracleParameter(":dob", record.DateOfBirth), New OracleParameter(":gender", record.Gender),
                    New OracleParameter(":addr", record.Address), New OracleParameter(":city", record.City),
                    New OracleParameter(":state", record.State), New OracleParameter(":pin", record.Pincode),
                    New OracleParameter(":tel", record.Telephone), New OracleParameter(":mob", record.Mobile),
                    New OracleParameter(":email", record.Email), New OracleParameter(":occ", record.Occupation),
                    New OracleParameter(":aadhar", record.AadharNumber), New OracleParameter(":ward", record.WardCircleSpecialRange),
                    New OracleParameter(":year", record.AssessmentYear), New OracleParameter(":updatedBy", record.UpdatedBy)
                }
                Return ExecuteNonQuery(sql, p)
            Else
                Dim sql = "INSERT INTO CLIENT_RECORD (CLIENT_CODE, FULL_NAME, PAN, DATE_OF_BIRTH, GENDER, ADDRESS, CITY, STATE, PINCODE, TELEPHONE, MOBILE, EMAIL, OCCUPATION, AADHAR_NUMBER, WARD_CIRCLE_SPECIAL_RANGE, ASSESSMENT_YEAR, CREATED_BY) VALUES (:code, :name, :pan, :dob, :gender, :addr, :city, :state, :pin, :tel, :mob, :email, :occ, :aadhar, :ward, :year, :createdBy)"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode), New OracleParameter(":name", record.FullName),
                    New OracleParameter(":pan", record.PAN), New OracleParameter(":dob", record.DateOfBirth),
                    New OracleParameter(":gender", record.Gender), New OracleParameter(":addr", record.Address),
                    New OracleParameter(":city", record.City), New OracleParameter(":state", record.State),
                    New OracleParameter(":pin", record.Pincode), New OracleParameter(":tel", record.Telephone),
                    New OracleParameter(":mob", record.Mobile), New OracleParameter(":email", record.Email),
                    New OracleParameter(":occ", record.Occupation), New OracleParameter(":aadhar", record.AadharNumber),
                    New OracleParameter(":ward", record.WardCircleSpecialRange), New OracleParameter(":year", record.AssessmentYear),
                    New OracleParameter(":createdBy", record.CreatedBy)
                }
                Return ExecuteNonQuery(sql, p)
            End If
        End Function

        Public Shared Function DeleteClient(clientCode As String) As Integer
            Return ExecuteNonQuery("DELETE FROM CLIENT_RECORD WHERE CLIENT_CODE = :code", New OracleParameter(":code", clientCode))
        End Function

        Public Shared Function GetAllTaxRecords(clientCode As String) As DataTable
            Dim sql = "SELECT * FROM INCOME_TAX_RECORD WHERE CLIENT_CODE = :code ORDER BY ASSESSMENT_YEAR DESC"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode)}
            Return ExecuteQuery(sql, p)
        End Function

        Public Shared Function InsertUpdateTaxRecord(record As Models.IncomeTaxRecord) As Integer
            Dim checkSql = "SELECT COUNT(*) FROM INCOME_TAX_RECORD WHERE CLIENT_CODE=:code AND ASSESSMENT_YEAR=:year"
            Dim count = Convert.ToInt32(ExecuteScalar(checkSql, New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear)))
            If count > 0 Then
                Dim sql = "UPDATE INCOME_TAX_RECORD SET FINANCIAL_YEAR=:fy, SALARY_INCOME=:sal, HOUSE_PROPERTY_INCOME=:hpi, BUSINESS_INCOME=:bi, CAPITAL_GAINS=:cg, OTHER_SOURCES_INCOME=:osi, TOTAL_INCOME=:ti, DEDUCTION_80C=:d80c, DEDUCTION_80D=:d80d, DEDUCTION_80G=:d80g, OTHER_DEDUCTIONS=:od, TOTAL_DEDUCTIONS=:tded, TAXABLE_INCOME=:taxi, TAX_ON_INCOME=:toi, REBATE_87A=:reb, SURCHARGE=:sur, HEALTH_EDU_CESS=:hec, TOTAL_TAX_LIABILITY=:ttl, TDS_DEDUCTED=:tds, ADVANCE_TAX_PAID=:atp, SELF_ASSESSMENT_TAX=:sat, REFUND_DUE=:ref, FILING_STATUS=:fs, FILING_DATE=:fd, RETURN_TYPE=:rt, REMARKS=:rem, UPDATED_DATE=SYSDATE WHERE CLIENT_CODE=:code AND ASSESSMENT_YEAR=:year"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear),
                    New OracleParameter(":fy", record.FinancialYear), New OracleParameter(":sal", record.SalaryIncome),
                    New OracleParameter(":hpi", record.HousePropertyIncome), New OracleParameter(":bi", record.BusinessIncome),
                    New OracleParameter(":cg", record.CapitalGains), New OracleParameter(":osi", record.OtherSourcesIncome),
                    New OracleParameter(":ti", record.TotalIncome), New OracleParameter(":d80c", record.Deduction80C),
                    New OracleParameter(":d80d", record.Deduction80D), New OracleParameter(":d80g", record.Deduction80G),
                    New OracleParameter(":od", record.OtherDeductions), New OracleParameter(":tded", record.TotalDeductions),
                    New OracleParameter(":taxi", record.TaxableIncome), New OracleParameter(":toi", record.TaxOnIncome),
                    New OracleParameter(":reb", record.Rebate87A), New OracleParameter(":sur", record.Surcharge),
                    New OracleParameter(":hec", record.HealthEduCess), New OracleParameter(":ttl", record.TotalTaxLiability),
                    New OracleParameter(":tds", record.TDSDeducted), New OracleParameter(":atp", record.AdvanceTaxPaid),
                    New OracleParameter(":sat", record.SelfAssessmentTax), New OracleParameter(":ref", record.RefundDue),
                    New OracleParameter(":fs", record.FilingStatus),
                    New OracleParameter(":fd", If(record.FilingDate = Date.MinValue, DBNull.Value, record.FilingDate)),
                    New OracleParameter(":rt", record.ReturnType), New OracleParameter(":rem", record.Remarks)
                }
                Return ExecuteNonQuery(sql, p)
            Else
                Dim sql = "INSERT INTO INCOME_TAX_RECORD (CLIENT_CODE, ASSESSMENT_YEAR, FINANCIAL_YEAR, SALARY_INCOME, HOUSE_PROPERTY_INCOME, BUSINESS_INCOME, CAPITAL_GAINS, OTHER_SOURCES_INCOME, TOTAL_INCOME, DEDUCTION_80C, DEDUCTION_80D, DEDUCTION_80G, OTHER_DEDUCTIONS, TOTAL_DEDUCTIONS, TAXABLE_INCOME, TAX_ON_INCOME, REBATE_87A, SURCHARGE, HEALTH_EDU_CESS, TOTAL_TAX_LIABILITY, TDS_DEDUCTED, ADVANCE_TAX_PAID, SELF_ASSESSMENT_TAX, REFUND_DUE, FILING_STATUS, RETURN_TYPE, REMARKS, CREATED_BY) VALUES (:code, :year, :fy, :sal, :hpi, :bi, :cg, :osi, :ti, :d80c, :d80d, :d80g, :od, :tded, :taxi, :toi, :reb, :sur, :hec, :ttl, :tds, :atp, :sat, :ref, :fs, :rt, :rem, :createdBy)"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear),
                    New OracleParameter(":fy", record.FinancialYear), New OracleParameter(":sal", record.SalaryIncome),
                    New OracleParameter(":hpi", record.HousePropertyIncome), New OracleParameter(":bi", record.BusinessIncome),
                    New OracleParameter(":cg", record.CapitalGains), New OracleParameter(":osi", record.OtherSourcesIncome),
                    New OracleParameter(":ti", record.TotalIncome), New OracleParameter(":d80c", record.Deduction80C),
                    New OracleParameter(":d80d", record.Deduction80D), New OracleParameter(":d80g", record.Deduction80G),
                    New OracleParameter(":od", record.OtherDeductions), New OracleParameter(":tded", record.TotalDeductions),
                    New OracleParameter(":taxi", record.TaxableIncome), New OracleParameter(":toi", record.TaxOnIncome),
                    New OracleParameter(":reb", record.Rebate87A), New OracleParameter(":sur", record.Surcharge),
                    New OracleParameter(":hec", record.HealthEduCess), New OracleParameter(":ttl", record.TotalTaxLiability),
                    New OracleParameter(":tds", record.TDSDeducted), New OracleParameter(":atp", record.AdvanceTaxPaid),
                    New OracleParameter(":sat", record.SelfAssessmentTax), New OracleParameter(":ref", record.RefundDue),
                    New OracleParameter(":fs", record.FilingStatus),
                    New OracleParameter(":rt", record.ReturnType), New OracleParameter(":rem", record.Remarks),
                    New OracleParameter(":createdBy", record.CreatedBy)
                }
                Return ExecuteNonQuery(sql, p)
            End If
        End Function

        Public Shared Function DeleteTaxRecord(clientCode As String, assessmentYear As String) As Integer
            Dim sql = "DELETE FROM INCOME_TAX_RECORD WHERE CLIENT_CODE = :code AND ASSESSMENT_YEAR = :year"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode), New OracleParameter(":year", assessmentYear)}
            Return ExecuteNonQuery(sql, p)
        End Function

        Public Shared Function GetTradingAccount(clientCode As String, assessmentYear As String) As DataTable
            Dim sql = "SELECT * FROM TRADING_ACCOUNT WHERE CLIENT_CODE = :code AND ASSESSMENT_YEAR = :year"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode), New OracleParameter(":year", assessmentYear)}
            Return ExecuteQuery(sql, p)
        End Function

        Public Shared Function InsertUpdateTradingAccount(record As Models.TradingAccount) As Integer
            Dim checkSql = "SELECT COUNT(*) FROM TRADING_ACCOUNT WHERE CLIENT_CODE=:code AND ASSESSMENT_YEAR=:year"
            Dim count = Convert.ToInt32(ExecuteScalar(checkSql, New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear)))
            If count > 0 Then
                Dim sql = "UPDATE TRADING_ACCOUNT SET OPENING_BALANCE=:ob, PURCHASES=:pur, PURCHASE_RETURN=:pr, GROSS_PURCHASES=:gp, CLOSING_STOCK=:cs, DIRECT_EXPENSES=:de, GROSS_PROFIT=:gprof, OTHER_INCOME=:oi, NET_PROFIT=:nprof, CREDITORS=:cred, SALES=:sal, SALES_RETURN=:sr, NET_SALES=:ns, DEBTORS=:deb, UPDATED_DATE=SYSDATE WHERE CLIENT_CODE=:code AND ASSESSMENT_YEAR=:year"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear),
                    New OracleParameter(":ob", record.OpeningBalance), New OracleParameter(":pur", record.Purchases),
                    New OracleParameter(":pr", record.PurchaseReturn), New OracleParameter(":gp", record.GrossPurchases),
                    New OracleParameter(":cs", record.ClosingStock), New OracleParameter(":de", record.DirectExpenses),
                    New OracleParameter(":gprof", record.GrossProfit), New OracleParameter(":oi", record.OtherIncome),
                    New OracleParameter(":nprof", record.NetProfit), New OracleParameter(":cred", record.Creditors),
                    New OracleParameter(":sal", record.Sales), New OracleParameter(":sr", record.SalesReturn),
                    New OracleParameter(":ns", record.NetSales), New OracleParameter(":deb", record.Debtors)
                }
                Return ExecuteNonQuery(sql, p)
            Else
                Dim sql = "INSERT INTO TRADING_ACCOUNT (CLIENT_CODE, ASSESSMENT_YEAR, OPENING_BALANCE, PURCHASES, PURCHASE_RETURN, GROSS_PURCHASES, CLOSING_STOCK, DIRECT_EXPENSES, GROSS_PROFIT, OTHER_INCOME, NET_PROFIT, CREDITORS, SALES, SALES_RETURN, NET_SALES, DEBTORS, CREATED_BY) VALUES (:code, :year, :ob, :pur, :pr, :gp, :cs, :de, :gprof, :oi, :nprof, :cred, :sal, :sr, :ns, :deb, :createdBy)"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear),
                    New OracleParameter(":ob", record.OpeningBalance), New OracleParameter(":pur", record.Purchases),
                    New OracleParameter(":pr", record.PurchaseReturn), New OracleParameter(":gp", record.GrossPurchases),
                    New OracleParameter(":cs", record.ClosingStock), New OracleParameter(":de", record.DirectExpenses),
                    New OracleParameter(":gprof", record.GrossProfit), New OracleParameter(":oi", record.OtherIncome),
                    New OracleParameter(":nprof", record.NetProfit), New OracleParameter(":cred", record.Creditors),
                    New OracleParameter(":sal", record.Sales), New OracleParameter(":sr", record.SalesReturn),
                    New OracleParameter(":ns", record.NetSales), New OracleParameter(":deb", record.Debtors),
                    New OracleParameter(":createdBy", record.CreatedBy)
                }
                Return ExecuteNonQuery(sql, p)
            End If
        End Function

        Public Shared Function GetPLAccount(clientCode As String, assessmentYear As String) As DataTable
            Dim sql = "SELECT * FROM PL_ACCOUNT WHERE CLIENT_CODE = :code AND ASSESSMENT_YEAR = :year"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode), New OracleParameter(":year", assessmentYear)}
            Return ExecuteQuery(sql, p)
        End Function

        Public Shared Function InsertUpdatePLAccount(record As Models.PLAccount) As Integer
            Dim checkSql = "SELECT COUNT(*) FROM PL_ACCOUNT WHERE CLIENT_CODE=:code AND ASSESSMENT_YEAR=:year"
            Dim count = Convert.ToInt32(ExecuteScalar(checkSql, New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear)))
            If count > 0 Then
                Dim sql = "UPDATE PL_ACCOUNT SET OPENING_STOCK=:os, PURCHASES=:pur, GROSS_PURCHASES=:gp, CLOSING_STOCK=:cs, COST_OF_GOODS_SOLD=:cogs, GROSS_PROFIT=:gprof, ADMINISTRATIVE_EXPENSES=:ae, SELLING_EXPENSES=:se, EMPLOYEE_BENEFIT_EXPENSES=:ebe, FINANCE_COSTS=:fc, DEPRECIATION=:dep, OTHER_EXPENSES=:oe, TOTAL_EXPENSES=:te, NET_PROFIT=:np, OTHER_INCOME=:oi, INTEREST_INCOME=:ii, DIVIDEND_INCOME=:di, UPDATED_DATE=SYSDATE WHERE CLIENT_CODE=:code AND ASSESSMENT_YEAR=:year"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear),
                    New OracleParameter(":os", record.OpeningStock), New OracleParameter(":pur", record.Purchases),
                    New OracleParameter(":gp", record.GrossPurchases), New OracleParameter(":cs", record.ClosingStock),
                    New OracleParameter(":cogs", record.CostOfGoodsSold), New OracleParameter(":gprof", record.GrossProfit),
                    New OracleParameter(":ae", record.AdministrativeExpenses), New OracleParameter(":se", record.SellingExpenses),
                    New OracleParameter(":ebe", record.EmployeeBenefitExpenses), New OracleParameter(":fc", record.FinanceCosts),
                    New OracleParameter(":dep", record.Depreciation), New OracleParameter(":oe", record.OtherExpenses),
                    New OracleParameter(":te", record.TotalExpenses), New OracleParameter(":np", record.NetProfit),
                    New OracleParameter(":oi", record.OtherIncome), New OracleParameter(":ii", record.InterestIncome),
                    New OracleParameter(":di", record.DividendIncome)
                }
                Return ExecuteNonQuery(sql, p)
            Else
                Dim sql = "INSERT INTO PL_ACCOUNT (CLIENT_CODE, ASSESSMENT_YEAR, OPENING_STOCK, PURCHASES, GROSS_PURCHASES, CLOSING_STOCK, COST_OF_GOODS_SOLD, GROSS_PROFIT, ADMINISTRATIVE_EXPENSES, SELLING_EXPENSES, EMPLOYEE_BENEFIT_EXPENSES, FINANCE_COSTS, DEPRECIATION, OTHER_EXPENSES, TOTAL_EXPENSES, NET_PROFIT, OTHER_INCOME, INTEREST_INCOME, DIVIDEND_INCOME, CREATED_BY) VALUES (:code, :year, :os, :pur, :gp, :cs, :cogs, :gprof, :ae, :se, :ebe, :fc, :dep, :oe, :te, :np, :oi, :ii, :di, :createdBy)"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear),
                    New OracleParameter(":os", record.OpeningStock), New OracleParameter(":pur", record.Purchases),
                    New OracleParameter(":gp", record.GrossPurchases), New OracleParameter(":cs", record.ClosingStock),
                    New OracleParameter(":cogs", record.CostOfGoodsSold), New OracleParameter(":gprof", record.GrossProfit),
                    New OracleParameter(":ae", record.AdministrativeExpenses), New OracleParameter(":se", record.SellingExpenses),
                    New OracleParameter(":ebe", record.EmployeeBenefitExpenses), New OracleParameter(":fc", record.FinanceCosts),
                    New OracleParameter(":dep", record.Depreciation), New OracleParameter(":oe", record.OtherExpenses),
                    New OracleParameter(":te", record.TotalExpenses), New OracleParameter(":np", record.NetProfit),
                    New OracleParameter(":oi", record.OtherIncome), New OracleParameter(":ii", record.InterestIncome),
                    New OracleParameter(":di", record.DividendIncome), New OracleParameter(":createdBy", record.CreatedBy)
                }
                Return ExecuteNonQuery(sql, p)
            End If
        End Function

        Public Shared Function GetBalanceSheet(clientCode As String, assessmentYear As String) As DataTable
            Dim sql = "SELECT * FROM BALANCE_SHEET WHERE CLIENT_CODE = :code AND ASSESSMENT_YEAR = :year"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode), New OracleParameter(":year", assessmentYear)}
            Return ExecuteQuery(sql, p)
        End Function

        Public Shared Function InsertUpdateBalanceSheet(record As Models.BalanceSheet) As Integer
            Dim checkSql = "SELECT COUNT(*) FROM BALANCE_SHEET WHERE CLIENT_CODE=:code AND ASSESSMENT_YEAR=:year"
            Dim count = Convert.ToInt32(ExecuteScalar(checkSql, New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear)))
            If count > 0 Then
                Dim sql = "UPDATE BALANCE_SHEET SET SHARE_CAPITAL=:sc, RESERVES_SURPLUS=:rs, SECURED_LOANS=:sl, UNSECURED_LOANS=:ul, CURRENT_LIABILITIES=:cl, TOTAL_LIABILITIES=:tl, FIXED_ASSETS=:fa, INVESTMENTS=:inv, INVENTORY=:inv2, DEBTORS=:deb, CASH_BANK_BALANCE=:cb, OTHER_CURRENT_ASSETS=:oca, TOTAL_ASSETS=:ta, CONTINGENT_LIABILITIES=:cont, UPDATED_DATE=SYSDATE WHERE CLIENT_CODE=:code AND ASSESSMENT_YEAR=:year"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear),
                    New OracleParameter(":sc", record.ShareCapital), New OracleParameter(":rs", record.ReservesSurplus),
                    New OracleParameter(":sl", record.SecuredLoans), New OracleParameter(":ul", record.UnsecuredLoans),
                    New OracleParameter(":cl", record.CurrentLiabilities), New OracleParameter(":tl", record.TotalLiabilities),
                    New OracleParameter(":fa", record.FixedAssets), New OracleParameter(":inv", record.Investments),
                    New OracleParameter(":inv2", record.Inventory), New OracleParameter(":deb", record.Debtors),
                    New OracleParameter(":cb", record.CashBankBalance), New OracleParameter(":oca", record.OtherCurrentAssets),
                    New OracleParameter(":ta", record.TotalAssets), New OracleParameter(":cont", record.ContingentLiabilities)
                }
                Return ExecuteNonQuery(sql, p)
            Else
                Dim sql = "INSERT INTO BALANCE_SHEET (CLIENT_CODE, ASSESSMENT_YEAR, SHARE_CAPITAL, RESERVES_SURPLUS, SECURED_LOANS, UNSECURED_LOANS, CURRENT_LIABILITIES, TOTAL_LIABILITIES, FIXED_ASSETS, INVESTMENTS, INVENTORY, DEBTORS, CASH_BANK_BALANCE, OTHER_CURRENT_ASSETS, TOTAL_ASSETS, CONTINGENT_LIABILITIES, CREATED_BY) VALUES (:code, :year, :sc, :rs, :sl, :ul, :cl, :tl, :fa, :inv, :inv2, :deb, :cb, :oca, :ta, :cont, :createdBy)"
                Dim p() As OracleParameter = {
                    New OracleParameter(":code", record.ClientCode), New OracleParameter(":year", record.AssessmentYear),
                    New OracleParameter(":sc", record.ShareCapital), New OracleParameter(":rs", record.ReservesSurplus),
                    New OracleParameter(":sl", record.SecuredLoans), New OracleParameter(":ul", record.UnsecuredLoans),
                    New OracleParameter(":cl", record.CurrentLiabilities), New OracleParameter(":tl", record.TotalLiabilities),
                    New OracleParameter(":fa", record.FixedAssets), New OracleParameter(":inv", record.Investments),
                    New OracleParameter(":inv2", record.Inventory), New OracleParameter(":deb", record.Debtors),
                    New OracleParameter(":cb", record.CashBankBalance), New OracleParameter(":oca", record.OtherCurrentAssets),
                    New OracleParameter(":ta", record.TotalAssets), New OracleParameter(":cont", record.ContingentLiabilities),
                    New OracleParameter(":createdBy", record.CreatedBy)
                }
                Return ExecuteNonQuery(sql, p)
            End If
        End Function

        Public Shared Function DeleteBalanceSheet(clientCode As String, assessmentYear As String) As Integer
            Dim sql = "DELETE FROM BALANCE_SHEET WHERE CLIENT_CODE = :code AND ASSESSMENT_YEAR = :year"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode), New OracleParameter(":year", assessmentYear)}
            Return ExecuteNonQuery(sql, p)
        End Function

        Public Shared Function DeletePLAccount(clientCode As String, assessmentYear As String) As Integer
            Dim sql = "DELETE FROM PL_ACCOUNT WHERE CLIENT_CODE = :code AND ASSESSMENT_YEAR = :year"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode), New OracleParameter(":year", assessmentYear)}
            Return ExecuteNonQuery(sql, p)
        End Function

        Public Shared Function DeleteTradingAccount(clientCode As String, assessmentYear As String) As Integer
            Dim sql = "DELETE FROM TRADING_ACCOUNT WHERE CLIENT_CODE = :code AND ASSESSMENT_YEAR = :year"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode), New OracleParameter(":year", assessmentYear)}
            Return ExecuteNonQuery(sql, p)
        End Function

        Public Shared Function DeleteTaxRecord(clientCode As String, assessmentYear As String) As Integer
            Dim sql = "DELETE FROM INCOME_TAX_RECORD WHERE CLIENT_CODE = :code AND ASSESSMENT_YEAR = :year"
            Dim p() As OracleParameter = {New OracleParameter(":code", clientCode), New OracleParameter(":year", assessmentYear)}
            Return ExecuteNonQuery(sql, p)
        End Function

        Public Shared Function GetAuditLog(tableName As String, recordId As Integer) As DataTable
            Dim sql = "SELECT * FROM (SELECT * FROM CLIENT_RECORD WHERE CLIENT_CODE = :id UNION ALL SELECT * FROM INCOME_TAX_RECORD WHERE CLIENT_CODE = :id UNION ALL SELECT * FROM TRADING_ACCOUNT WHERE CLIENT_CODE = :id UNION ALL SELECT * FROM PL_ACCOUNT WHERE CLIENT_CODE = :id UNION ALL SELECT * FROM BALANCE_SHEET WHERE CLIENT_CODE = :id)"
            Return ExecuteQuery(sql, New OracleParameter(":id", recordId))
        End Function

    End Class

End Namespace
