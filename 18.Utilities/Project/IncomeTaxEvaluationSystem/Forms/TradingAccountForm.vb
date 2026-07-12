Public Class TradingAccountForm
    Private Sub btnSave_Click(sender As Object, e As EventArgs) Handles btnSave.Click
        Dim record As New Models.TradingAccount()
        record.ClientCode = cmbClient.Text.Split("-"c)(0).Trim()
        record.AssessmentYear = txtAY.Text.Trim()
        record.OpeningBalance = CDec(txtOB.Text)
        record.Purchases = CDec(txtPurchases.Text)
        record.Sales = CDec(txtSales.Text)
        record.CreatedBy = MainForm.UserId
        Data.OracleDataAccess.InsertUpdateTradingAccount(record)
        MessageBox.Show("Trading account saved", "Info", MessageBoxButtons.OK, MessageBoxIcon.Information)
    End Sub

    Private Sub TradingAccountForm_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Dim dt = Data.OracleDataAccess.GetAllClients()
        cmbClient.Items.Clear()
        For Each row As DataRowView In dt.DefaultView
            cmbClient.Items.Add(row("CLIENT_CODE").ToString() + " - " + row("FULL_NAME").ToString())
        Next
    End Sub
End Class