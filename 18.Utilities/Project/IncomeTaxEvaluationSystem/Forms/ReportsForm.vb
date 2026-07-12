Public Class ReportsForm
    Private Sub btnGenerate_Click(sender As Object, e As EventArgs) Handles btnGenerate.Click
        Dim rptType = cmbType.Text
        Dim clientCode = cmbClient.Text.Split("-"c)(0).Trim()
        Dim dt As DataTable = Nothing
        If rptType = "Clients" Then
            dt = Data.OracleDataAccess.GetAllClients()
        ElseIf rptType = "Tax Records" Then
            dt = Data.OracleDataAccess.GetAllTaxRecords(clientCode)
        End If
        If dt IsNot Nothing Then
            dgvReport.DataSource = dt
            Reports.ReportGenerator.ExportToCsv(dt, rptType + "_Report.csv")
        End If
    End Sub
End Class