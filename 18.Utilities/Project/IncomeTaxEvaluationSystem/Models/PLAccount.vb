Namespace Models
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
        Public Property CreatedBy As String = String.Empty
    End Class
End Namespace