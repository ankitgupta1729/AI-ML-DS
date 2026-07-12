Public Class MainForm
    Public Shared UserId As String = String.Empty
    Public Shared UserName As String = String.Empty
    Public Shared UserRole As String = String.Empty

    Private Sub MainForm_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        lblUser.Text = "Welcome, " + UserName
    End Sub

    Private Sub btnClients_Click(sender As Object, e As EventArgs) Handles btnClients.Click
        Dim frm As New ClientRecordForm()
        frm.ShowDialog()
    End Sub

    Private Sub btnTax_Click(sender As Object, e As EventArgs) Handles btnTax.Click
        Dim frm As New IncomeTaxRecordForm()
        frm.ShowDialog()
    End Sub

    Private Sub btnTrading_Click(sender As Object, e As EventArgs) Handles btnTrading.Click
        Dim frm As New TradingAccountForm()
        frm.ShowDialog()
    End Sub

    Private Sub btnPL_Click(sender As Object, e As EventArgs) Handles btnPL.Click
        Dim frm As New PLAccountForm()
        frm.ShowDialog()
    End Sub

    Private Sub btnBS_Click(sender As Object, e As EventArgs) Handles btnBS.Click
        Dim frm As New BalanceSheetForm()
        frm.ShowDialog()
    End Sub

    Private Sub btnReports_Click(sender As Object, e As EventArgs) Handles btnReports.Click
        Dim frm As New ReportsForm()
        frm.ShowDialog()
    End Sub

    Private Sub btnLogout_Click(sender As Object, e As EventArgs) Handles btnLogout.Click
        Me.Close()
        Application.Restart()
    End Sub
End Class