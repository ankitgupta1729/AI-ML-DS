' =============================================================================
' ITEMS · Login.aspx.vb — Forms authentication against APP_USER (SRS §7)
' =============================================================================
Imports System.Web.Security
Imports ITEMS.Logic

Namespace ITEMS

    Partial Public Class LoginPage
        Inherits System.Web.UI.Page

        Protected Sub btnLogin_Click(sender As Object, e As EventArgs)
            Dim fullName = Security.Authenticate(txtUser.Text, txtPass.Text)
            If String.IsNullOrEmpty(fullName) Then
                litErr.Text = "Invalid user id or password. Please try again."
                Return
            End If
            ' Store the display name as the identity so the shell can greet the user.
            FormsAuthentication.SetAuthCookie(fullName, False)
            Dim target = Request.QueryString("ReturnUrl")
            Response.Redirect(If(String.IsNullOrEmpty(target), "~/Default.aspx", target))
        End Sub

    End Class

End Namespace
