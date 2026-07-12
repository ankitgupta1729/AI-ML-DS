Namespace Models

    Public Class ClientRecord
        Public Property ID As Integer = 0
        Public Property ClientCode As String = String.Empty
        Public Property FullName As String = String.Empty
        Public Property PAN As String = String.Empty
        Public Property DateOfBirth As Date = Date.MinValue
        Public Property Gender As String = String.Empty
        Public Property Address As String = String.Empty
        Public Property City As String = String.Empty
        Public Property State As String = String.Empty
        Public Property Pincode As String = String.Empty
        Public Property Telephone As String = String.Empty
        Public Property Mobile As String = String.Empty
        Public Property Email As String = String.Empty
        Public Property Occupation As String = String.Empty
        Public Property AadharNumber As String = String.Empty
        Public Property WardCircleSpecialRange As String = String.Empty
        Public Property AssessmentYear As String = String.Empty
        Public Property CreatedDate As Date = Date.MinValue
        Public Property UpdatedDate As Date = Date.MinValue
        Public Property CreatedBy As String = String.Empty
        Public Property UpdatedBy As String = String.Empty
    End Class

    Public Class IncomeTaxRecord
        Public Property ID As Integer = 0
        Public Property ClientCode As String = String.Empty
        Public Property AssessmentYear As String = String.Empty
        Public Property FinancialYear As String = String.Empty
        Public Property SalaryIncome As Decimal = 0D
        Public Property HousePropertyIncome As Decimal = 0D
        Public Property BusinessIncome As Decimal = 0D
        Public Property CapitalGains As Decimal = 0D
        Public Property OtherSourcesIncome As Decimal = 0D
        Public Property TotalIncome As Decimal = 0D
        Public Property Deduction80C As Decimal = 0D
        Public Property Deduction80D As Decimal = 0D
        Public Property Deduction80G As Decimal = 0D
        Public Property OtherDeductions As Decimal = 0D
        Public Property TotalDeductions As Decimal = 0D
        Public Property TaxableIncome As Decimal = 0D
        Public Property TaxOnIncome As Decimal = 0D
        Public Property Rebate87A As Decimal = 0D
        Public Property Surcharge As Decimal = 0D
        Public Property HealthEduCess As Decimal = 0D
        Public Property TotalTaxLiability As Decimal = 0D
        Public Property TDSDeducted As Decimal = 0D
        Public Property AdvanceTaxPaid As Decimal = 0D
        Public Property SelfAssessmentTax As Decimal = 0D
        Public Property RefundDue As Decimal = 0D
        Public Property FilingStatus As String = "Pending"
        Public Property FilingDate As Date = Date.MinValue
        Public Property ReturnType As String = String.Empty
        Public Property VerifiedBy As String = String.Empty
        Public Property Remarks As String = String.Empty
        Public Property CreatedDate As Date = Date.MinValue
        Public Property UpdatedDate As Date = Date.MinValue
        Public Property CreatedBy As String = String.Empty
    End Class

    Public Class TradingAccount
        Public Property ID As Integer = 0
        Public Property ClientCode As String = String.Empty
        Public Property AssessmentYear As String = String.Empty
        Public Property OpeningBalance As Decimal = 0D
        Public Property Purchases As Decimal = 0D
        Public Property PurchaseReturn As Decimal = 0D
        Public Property GrossPurchases As Decimal = 0D
        Public Property ClosingStock As Decimal = 0D
        Public Property DirectExpenses As Decimal = 0D
        Public Property GrossProfit As Decimal = 0D
        Public Property OtherIncome As Decimal = 0D
        Public Property NetProfit As Decimal = 0D
        Public Property Creditors As Decimal = 0D
        Public Property Sales As Decimal = 0D
        Public Property SalesReturn As Decimal = 0D
        Public Property NetSales As Decimal = 0D
        Public Property Debtors As Decimal = 0D
        Public Property CreatedDate As Date = Date.MinValue
        Public Property UpdatedDate As Date = Date.MinValue
        Public Property CreatedBy As String = String.Empty
    End Class

    Public Class PLAccount
        Public Property ID As Integer = 0
        Public Property ClientCode As String = String.Empty
        Public Property AssessmentYear As String = String.Empty
        Public Property OpeningStock As Decimal = 0D
        Public Property Purchases As Decimal = 0D
        Public Property GrossPurchases As Decimal = 0D
        Public Property ClosingStock As Decimal = 0D
        Public Property CostOfGoodsSold As Decimal = 0D
        Public Property GrossProfit As Decimal = 0D
        Public Property AdministrativeExpenses As Decimal = 0D
        Public Property SellingExpenses As Decimal = 0D
        Public Property EmployeeBenefitExpenses As Decimal = 0D
        Public Property FinanceCosts As Decimal = 0D
        Public Property Depreciation As Decimal = 0D
        Public Property OtherExpenses As Decimal = 0D
        Public Property TotalExpenses As Decimal = 0D
        Public Property NetProfit As Decimal = 0D
        Public Property OtherIncome As Decimal = 0D
        Public Property InterestIncome As Decimal = 0D
        Public Property DividendIncome As Decimal = 0D
        Public Property CreatedDate As Date = Date.MinValue
        Public Property UpdatedDate As Date = Date.MinValue
        Public Property CreatedBy As String = String.Empty
    End Class

    Public Class BalanceSheet
        Public Property ID As Integer = 0
        Public Property ClientCode As String = String.Empty
        Public Property AssessmentYear As String = String.Empty
        Public Property ShareCapital As Decimal = 0D
        Public Property ReservesSurplus As Decimal = 0D
        Public Property SecuredLoans As Decimal = 0D
        Public Property UnsecuredLoans As Decimal = 0D
        Public Property CurrentLiabilities As Decimal = 0D
        Public Property TotalLiabilities As Decimal = 0D
        Public Property FixedAssets As Decimal = 0D
        Public Property Investments As Decimal = 0D
        Public Property Inventory As Decimal = 0D
        Public Property Debtors As Decimal = 0D
        Public Property CashBankBalance As Decimal = 0D
        Public Property OtherCurrentAssets As Decimal = 0D
        Public Property TotalAssets As Decimal = 0D
        Public Property ContingentLiabilities As String = String.Empty
        Public Property CreatedDate As Date = Date.MinValue
        Public Property UpdatedDate As Date = Date.MinValue
        Public Property CreatedBy As String = String.Empty
    End Class

End Namespace
