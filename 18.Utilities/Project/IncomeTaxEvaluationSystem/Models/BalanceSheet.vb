Namespace Models
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
        Public Property CreatedBy As String = String.Empty
    End Class
End Namespace