' =============================================================================
' ITEMS · TaxEngine.vb — income-tax computation (old regime, AY 2024-25)
' Server-side port of the browser engine used in the web demo, so the figures
' match. Gross Total Income -> deductions -> Total Income -> slab tax ->
' rebate 87A -> surcharge -> health & education cess -> net & balance.
' =============================================================================
Namespace Logic

    Public Class TaxResult
        Public Property GrossTotalIncome As Decimal
        Public Property TotalIncome As Decimal
        Public Property IncomeAtNormalRate As Decimal
        Public Property TaxAtNormalRate As Decimal
        Public Property IncomeAtSpecialRate As Decimal
        Public Property TaxAtSpecialRate As Decimal
        Public Property TaxOnTotalIncome As Decimal
        Public Property Rebate87A As Decimal
        Public Property TaxPayable As Decimal
        Public Property Surcharge As Decimal
        Public Property Cess As Decimal
        Public Property TotalTaxPayable As Decimal
        Public Property NetTaxPayable As Decimal
        Public Property BalancePayableOrRefund As Decimal
    End Class

    Public NotInheritable Class TaxEngine

        Private Const CESS_RATE As Decimal = 0.04D
        Private Const REBATE_LIMIT As Decimal = 500000D
        Private Const REBATE_MAX As Decimal = 12500D
        Private Const FIRM_RATE As Decimal = 0.3D

        Private Shared ReadOnly SlabUpto() As Decimal = {250000D, 500000D, 1000000D, Decimal.MaxValue}
        Private Shared ReadOnly SlabRate() As Decimal = {0D, 0.05D, 0.2D, 0.3D}

        Private Sub New()
        End Sub

        Public Shared Function SlabTax(income As Decimal) As Decimal
            Dim tax As Decimal = 0D, lower As Decimal = 0D
            For i = 0 To SlabUpto.Length - 1
                If income > lower Then
                    Dim band = Math.Min(income, SlabUpto(i)) - lower
                    tax += band * SlabRate(i)
                    lower = SlabUpto(i)
                Else
                    Exit For
                End If
            Next
            Return Math.Round(tax)
        End Function

        Private Shared Function SurchargeRate(ti As Decimal) As Decimal
            If ti > 50000000D Then Return 0.37D
            If ti > 20000000D Then Return 0.25D
            If ti > 10000000D Then Return 0.15D
            If ti > 5000000D Then Return 0.1D
            Return 0D
        End Function

        ''' <summary>Computes the tax for a return. isFirm applies the flat firm rate.</summary>
        Public Shared Function Compute(r As Models.ReturnRecord, isFirm As Boolean) As TaxResult
            Dim capital = If(r.TotalCapitalGains <> 0, r.TotalCapitalGains, r.ShortTermGain + r.LongTermGain)
            Dim gross = r.IncomeFromSalary + r.IncomeFromHouseProperty + r.IncomeFromBusiness +
                        capital + r.IncomeFromOtherSources + r.OtherPersonIncome
            Dim deductions = Math.Min(r.DeductionUnderVIA, gross)
            Dim totalIncome = Math.Max(0D, gross - deductions)

            Dim spclBase = r.LongTermGain
            Dim normalBase = Math.Max(0D, totalIncome - spclBase)

            Dim taxNormal = If(isFirm, Math.Round(totalIncome * FIRM_RATE), SlabTax(normalBase))
            Dim taxSpecial = If(isFirm, 0D, Math.Round(spclBase * 0.2D))
            Dim taxOnTotal = taxNormal + taxSpecial

            Dim rebate As Decimal = 0D
            If Not isFirm AndAlso totalIncome <= REBATE_LIMIT Then rebate = Math.Min(taxOnTotal, REBATE_MAX)

            Dim taxPayable = Math.Max(0D, taxOnTotal - rebate)
            Dim surcharge = Math.Round(taxPayable * SurchargeRate(totalIncome))
            Dim cess = Math.Round((taxPayable + surcharge) * CESS_RATE)
            Dim totalTax = taxPayable + surcharge + cess

            Dim netTax = Math.Max(0D, totalTax - r.Relief)
            Dim balance = netTax + r.InterestPayable - r.TdsAtSource - r.AdvanceTaxPaid - r.SelfAssessmentPaid

            Return New TaxResult With {
                .GrossTotalIncome = gross, .TotalIncome = totalIncome,
                .IncomeAtNormalRate = normalBase, .TaxAtNormalRate = taxNormal,
                .IncomeAtSpecialRate = spclBase, .TaxAtSpecialRate = taxSpecial,
                .TaxOnTotalIncome = taxOnTotal, .Rebate87A = rebate, .TaxPayable = taxPayable,
                .Surcharge = surcharge, .Cess = cess, .TotalTaxPayable = totalTax,
                .NetTaxPayable = netTax, .BalancePayableOrRefund = Math.Round(balance)
            }
        End Function

    End Class

End Namespace
