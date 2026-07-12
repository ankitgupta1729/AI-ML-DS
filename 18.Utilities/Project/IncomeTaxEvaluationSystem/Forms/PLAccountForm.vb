Public Class PLAccountForm
    Private Sub btnSave_Click(sender As Object, e As EventArgs) Handles btnSave.Click
        If cmbClient.SelectedIndex < 0 Then
            MessageBox.Show("Please select a client", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        Dim record As New Models.PLAccount()
        record.ClientCode = cmbClient.Text.Split("-"c)(0).Trim()
        record.AssessmentYear = txtAY.Text.Trim()
        Dim np As Decimal
        If Not Decimal.TryParse(txtNetProfit.Text, np) Then
            MessageBox.Show("Please enter a valid numeric value for Net Profit", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        record.NetProfit = np
        record.CreatedBy = MainForm.UserId
        Data.OracleDataAccess.InsertUpdatePLAccount(record)
        MessageBox.Show("P&L saved", "Info", MessageBoxButtons.OK, MessageBoxIcon.Information)
    End Sub

    Private Sub PLAccountForm_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Dim dt = Data.OracleDataAccess.GetAllClients()
        cmbClient.Items.Clear()
        For Each row As DataRowView In dt.DefaultView
            cmbClient.Items.Add(row("CLIENT_CODE").ToString() + " - " + row("FULL_NAME").ToString())
        Next
    End Sub
End Class