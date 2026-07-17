' =============================================================================
' Income Tax Evaluation System · Security.vb — authentication against APP_USER (SRS §7 & §15)
' Passwords are verified against stored SHA-256 hashes; never compared in clear.
' =============================================================================
Imports System.Security.Cryptography
Imports System.Text
Imports ITEMS.Data

Namespace Logic

    Public NotInheritable Class Security

        Private Sub New()
        End Sub

        Public Shared Function Sha256(text As String) As String
            Using sha = SHA256.Create()
                Dim bytes = sha.ComputeHash(Encoding.UTF8.GetBytes(If(text, "")))
                Dim sb As New StringBuilder(bytes.Length * 2)
                For Each b In bytes
                    sb.Append(b.ToString("x2"))
                Next
                Return sb.ToString()
            End Using
        End Function

        ''' <summary>Returns the user's full name on success, or Nothing.</summary>
        Public Shared Function Authenticate(username As String, password As String) As String
            If String.IsNullOrWhiteSpace(username) Then Return Nothing
            Dim row = OracleDb.QueryRow(
                "SELECT FULL_NAME, PASSWORD_HASH, ROLE FROM APP_USER WHERE USERNAME = :u AND IS_ACTIVE = 'Y'",
                OracleDb.PStr("u", username.Trim().ToLowerInvariant()))
            If row Is Nothing Then Return Nothing
            If Not String.Equals(Convert.ToString(row("PASSWORD_HASH")), Sha256(password), StringComparison.OrdinalIgnoreCase) Then
                Return Nothing
            End If
            Return Convert.ToString(row("FULL_NAME"))
        End Function

    End Class

End Namespace
