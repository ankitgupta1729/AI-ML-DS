Namespace Models
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
        Public Property CreatedBy As String = String.Empty
    End Class
End Namespace