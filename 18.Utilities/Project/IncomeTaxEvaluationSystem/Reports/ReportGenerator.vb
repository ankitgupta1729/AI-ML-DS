Namespace Reports
    Public Class ReportGenerator
        Public Shared Sub ExportToCsv(dt As DataTable, filename As String)
            Dim sb As New System.Text.StringBuilder()
            For Each col As DataColumn In dt.Columns
                sb.Append(col.ColumnName + ",")
            Next
            sb.AppendLine()
            For Each row As DataRow In dt.Rows
                For Each col As DataColumn In dt.Columns
                    sb.Append(Convert.ToString(row(col)) + ",")
                Next
                sb.AppendLine()
            Next
            System.IO.File.WriteAllText(filename, sb.ToString())
            MessageBox.Show("Exported to " + filename, "Export", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End Sub
    End Class
End Namespace