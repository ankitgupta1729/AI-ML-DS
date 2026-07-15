' =============================================================================
' ITEMS · Models.vb — plain data objects for the seven modules
' =============================================================================
Namespace Models

    Public Enum ClientCategory
        Individual = 0
        HUF = 1
        Firm = 2
        AOP = 3
        LocalAuthority = 4
    End Enum

    Public Class Client
        Public Property Pan As String
        Public Property Name As String
        Public Property FathersName As String
        Public Property Dob As Date?
        Public Property Pincode As String
        Public Property Address As String
        Public Property Telephone As String
        Public Property Sex As Integer = 1                 ' 1 = Male, 0 = Female
        Public Property Category As Integer = 0            ' ClientCategory
        Public Property Residence As Integer = 0           ' 0=R 1=NR 2=NOR
        Public Property WardCircleRange As String

        Public ReadOnly Property IsFirm As Boolean
            Get
                Return Category = ClientCategory.Firm
            End Get
        End Property

        Public ReadOnly Property CategoryText As String
            Get
                Select Case Category
                    Case 0 : Return "Individual"
                    Case 1 : Return "HUF"
                    Case 2 : Return "Firm"
                    Case 3 : Return "AOP"
                    Case Else : Return "Local Authority"
                End Select
            End Get
        End Property
    End Class

    ''' <summary>INCOME_TAX_RECORD — only the fields the UI edits are modelled;
    ''' the computed columns are written back from TaxResult on save.</summary>
    Public Class ReturnRecord
        Public Property Pan As String
        Public Property AyFrom As Date
        Public Property AyTo As Date
        Public Property ReturnType As Integer = 0          ' 0 = Original, 1 = Revised

        Public Property IncomeFromSalary As Decimal
        Public Property IncomeFromHouseProperty As Decimal
        Public Property IncomeFromBusiness As Decimal
        Public Property ShortTermGain As Decimal
        Public Property LongTermGain As Decimal
        Public Property TotalCapitalGains As Decimal
        Public Property IncomeFromOtherSources As Decimal
        Public Property OtherPersonIncome As Decimal
        Public Property DeductionUnderVIA As Decimal

        Public Property TdsAtSource As Decimal
        Public Property AdvanceTaxPaid As Decimal
        Public Property SelfAssessmentPaid As Decimal
        Public Property InterestPayable As Decimal
        Public Property Relief As Decimal

        ' Written from the TaxEngine result on save.
        Public Property GrossTotalIncome As Decimal
        Public Property TotalIncome As Decimal
        Public Property NetTaxPayable As Decimal
        Public Property BalancePayableRefund As Decimal

        Public ReadOnly Property ReturnTypeText As String
            Get
                Return If(ReturnType = 1, "Revised", "Original")
            End Get
        End Property

        Public ReadOnly Property AssessmentYear As String
            Get
                Return AyFrom.ToString("yyyy") & "-" & AyTo.ToString("yy")
            End Get
        End Property
    End Class

End Namespace
