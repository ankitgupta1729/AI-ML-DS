Public Class TradingAccountForm
    Private Sub btnSave_Click(sender As Object, e As EventArgs) Handles btnSave.Click
        If cmbClient.SelectedIndex < 0 Then
            MessageBox.Show("Please select a client", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        Dim record As New Models.TradingAccount()
        record.ClientCode = cmbClient.Text.Split("-"c)(0).Trim()
        record.AssessmentYear = txtAY.Text.Trim()
        Dim ob As Decimal, pur As Decimal, sal As Decimal
        If Not Decimal.TryParse(txtOB.Text, ob) OrElse Not Decimal.TryParse(txtPurchases.Text, pur) OrElse
           Not Decimal.TryParse(txtSales.Text, sal) Then
            MessageBox.Show("Please enter valid numeric values for all amount fields", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        record.OpeningBalance = ob
        record.Purchases = pur
        record.Sales = sal
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