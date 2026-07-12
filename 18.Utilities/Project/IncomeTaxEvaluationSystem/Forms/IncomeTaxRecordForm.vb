Public Class IncomeTaxRecordForm
    Private Sub btnSave_Click(sender As Object, e As EventArgs) Handles btnSave.Click
        Dim record As New Models.IncomeTaxRecord()
        record.ClientCode = cmbClient.Text.Split("-"c)(0).Trim()
        record.AssessmentYear = txtAY.Text.Trim()
        record.SalaryIncome = CDec(txtSalary.Text)
        record.HousePropertyIncome = CDec(txtHouse.Text)
        record.BusinessIncome = CDec(txtBusiness.Text)
        record.CapitalGains = CDec(txtCapital.Text)
        record.OtherSourcesIncome = CDec(txtOther.Text)
        record.TotalIncome = record.SalaryIncome + record.HousePropertyIncome + record.BusinessIncome + record.CapitalGains + record.OtherSourcesIncome
        record.Deduction80C = CDec(txt80C.Text)
        record.Deduction80D = CDec(txt80D.Text)
        record.Deduction80G = CDec(txt80G.Text)
        record.OtherDeductions = CDec(txtOtherDed.Text)
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