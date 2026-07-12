Public Class BalanceSheetForm
    Private Sub btnSave_Click(sender As Object, e As EventArgs) Handles btnSave.Click
        If cmbClient.SelectedIndex < 0 Then
            MessageBox.Show("Please select a client", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        Dim record As New Models.BalanceSheet()
        record.ClientCode = cmbClient.Text.Split("-"c)(0).Trim()
        record.AssessmentYear = txtAY.Text.Trim()
        Dim tl As Decimal, ta As Decimal
        If Not Decimal.TryParse(txtLiabilities.Text, tl) OrElse Not Decimal.TryParse(txtAssets.Text, ta) Then
            MessageBox.Show("Please enter valid numeric values for Liabilities and Assets", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        record.TotalLiabilities = tl
        record.TotalAssets = ta
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