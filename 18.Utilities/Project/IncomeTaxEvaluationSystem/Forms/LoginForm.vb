Public Class LoginForm

    Private Sub btnLogin_Click(sender As Object, e As EventArgs) Handles btnLogin.Click
        Dim userId = txtUserId.Text.Trim()
        Dim password = txtPassword.Text.Trim()
        If String.IsNullOrEmpty(userId) OrElse String.IsNullOrEmpty(password) Then
            MessageBox.Show("Please enter User ID and Password", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        Dim dt As DataTable = Data.OracleDataAccess.ValidateUser(userId, password)
        If dt.Rows.Count > 0 Then
            Dim userName = dt.Rows(0)("FULL_NAME").ToString()
            MainForm.UserId = userId
            MainForm.UserName = userName
            MainForm.UserRole = dt.Rows(0)("ROLE").ToString()
            Dim main As New MainForm()
            main.Show()
            Me.Hide()
        Else
            MessageBox.Show("Invalid User ID or Password", "Login Failed", MessageBoxButtons.OK, MessageBoxIcon.Error)
        End If
    End Sub

    Private Sub btnExit_Click(sender As Object, e As EventArgs) Handles btnExit.Click
        Application.Exit()
    End Sub

    Private Sub txtPassword_KeyDown(sender As Object, e As KeyEventArgs) Handles txtPassword.KeyDown
        If e.KeyCode = Keys.Enter Then btnLogin.PerformClick()
    End Sub

End Class
