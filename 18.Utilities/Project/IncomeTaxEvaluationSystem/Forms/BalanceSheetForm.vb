Public Class BalanceSheetForm
    Private Sub btnSave_Click(sender As Object, e As EventArgs) Handles btnSave.Click
        Dim record As New Models.BalanceSheet()
        record.ClientCode = cmbClient.Text.Split("-"c)(0).Trim()
        record.AssessmentYear = txtAY.Text.Trim()
        record.TotalLiabilities = CDec(txtLiabilities.Text)
        record.TotalAssets = CDec(txtAssets.Text)
        record.CreatedBy = MainForm.UserId
        Data.OracleDataAccess.InsertUpdateBalanceSheet(record)
        MessageBox.Show("Balance sheet saved", "Info", MessageBoxButtons.OK, MessageBoxIcon.Information)
    End Sub

    Private Sub BalanceSheetForm_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Dim dt = Data.OracleDataAccess.GetAllClients()
        cmbClient.Items.Clear()
        For Each row As DataRowView In dt.DefaultView
            cmbClient.Items.Add(row("CLIENT_CODE").ToString() + " - " + row("FULL_NAME").ToString())
        Next
    End Sub
End Class