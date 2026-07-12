Public Class IncomeTaxRecordForm
    Private Sub btnSave_Click(sender As Object, e As EventArgs) Handles btnSave.Click
        If cmbClient.SelectedIndex < 0 Then
            MessageBox.Show("Please select a client", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        Dim record As New Models.IncomeTaxRecord()
        record.ClientCode = cmbClient.Text.Split("-"c)(0).Trim()
        record.AssessmentYear = txtAY.Text.Trim()
        Dim sal As Decimal, hpi As Decimal, bi As Decimal, cg As Decimal, osi As Decimal
        Dim d80c As Decimal, d80d As Decimal, d80g As Decimal, od As Decimal
        If Not Decimal.TryParse(txtSalary.Text, sal) OrElse Not Decimal.TryParse(txtHouse.Text, hpi) OrElse
           Not Decimal.TryParse(txtBusiness.Text, bi) OrElse Not Decimal.TryParse(txtCapital.Text, cg) OrElse
           Not Decimal.TryParse(txtOther.Text, osi) OrElse Not Decimal.TryParse(txt80C.Text, d80c) OrElse
           Not Decimal.TryParse(txt80D.Text, d80d) OrElse Not Decimal.TryParse(txt80G.Text, d80g) OrElse
           Not Decimal.TryParse(txtOtherDed.Text, od) Then
            MessageBox.Show("Please enter valid numeric values for all income and deduction fields", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        record.SalaryIncome = sal
        record.HousePropertyIncome = hpi
        record.BusinessIncome = bi
        record.CapitalGains = cg
        record.OtherSourcesIncome = osi
        record.TotalIncome = sal + hpi + bi + cg + osi
        record.Deduction80C = d80c
        record.Deduction80D = d80d
        record.Deduction80G = d80g
        record.OtherDeductions = od
        record.TotalDeductions = d80c + d80d + d80g + od
        record.TaxableIncome = record.TotalIncome - record.TotalDeductions
        record.CreatedBy = MainForm.UserId
        Data.OracleDataAccess.InsertUpdateTaxRecord(record)
        MessageBox.Show("Tax record saved", "Info", MessageBoxButtons.OK, MessageBoxIcon.Information)
    End Sub

    Private Sub IncomeTaxRecordForm_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Dim dt = Data.OracleDataAccess.GetAllClients()
        cmbClient.Items.Clear()
        For Each row As DataRowView In dt.DefaultView
            cmbClient.Items.Add(row("CLIENT_CODE").ToString() + " - " + row("FULL_NAME").ToString())
        Next
    End Sub
End Class