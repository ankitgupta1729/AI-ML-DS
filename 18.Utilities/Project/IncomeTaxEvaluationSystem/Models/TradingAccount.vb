Namespace Models
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
        Public Property CreatedBy As String = String.Empty
    End Class
End Namespace