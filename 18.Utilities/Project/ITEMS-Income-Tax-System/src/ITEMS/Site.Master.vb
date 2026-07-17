' =============================================================================
' Income Tax Evaluation System · Site.Master.vb — shared shell (sidebar, top bar, sign-out)
' =============================================================================
Imports System.Web.Security
Imports System.Web.UI
Imports System.Web.UI.WebControls

Namespace ITEMS

    Partial Public Class SiteMaster
        Inherits System.Web.UI.MasterPage

        Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
            Dim name = If(Page.User IsNot Nothing AndAlso Page.User.Identity.IsAuthenticated,
                          Page.User.Identity.Name, "User")
            litUser.Text = Server.HtmlEncode(name)
            litInitial.Text = Server.HtmlEncode(If(String.IsNullOrEmpty(name), "U", name.Substring(0, 1).ToUpperInvariant()))
        End Sub

        Protected Sub btnLogout_Click(sender As Object, e As EventArgs)
            FormsAuthentication.SignOut()
            Session.Abandon()
            Response.Redirect("~/Login.aspx")
        End Sub

    End Class

End Namespace
