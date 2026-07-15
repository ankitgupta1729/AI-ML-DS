' =============================================================================
' ITEMS · Clients.aspx.vb — list, search and delete clients
' =============================================================================
Imports System.Data
Imports ITEMS.Data
Imports ITEMS.Repositories

Namespace ITEMS

    Partial Public Class ClientsPage
        Inherits System.Web.UI.Page

        Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
            If Not IsPostBack Then Bind()
        End Sub

        Private Sub Bind()
            Dim sql = "SELECT PAN, CLIENT_NAME, DOB, WARD_CIRCLE_SPECIAL_RANGE, " &
                      "CASE INDV_HUF_FIRM_AOP_LA WHEN 0 THEN 'Individual' WHEN 1 THEN 'HUF' WHEN 2 THEN 'Firm' " &
                      "WHEN 3 THEN 'AOP' ELSE 'Local Authority' END AS CATEGORY_TEXT FROM CLIENT_RECORD "
            Dim dt As DataTable
            Dim q = txtSearch.Text.Trim()
            If q = "" Then
                dt = OracleDb.Query(sql & "ORDER BY CLIENT_NAME")
            Else
                dt = OracleDb.Query(sql & "WHERE UPPER(CLIENT_NAME) LIKE :q OR UPPER(PAN) LIKE :q OR UPPER(ADDRESS) LIKE :q ORDER BY CLIENT_NAME",
                                    OracleDb.PStr("q", "%" & q.ToUpperInvariant() & "%"))
            End If
            gv.DataSource = dt
            gv.DataBind()
        End Sub

        Protected Sub txtSearch_TextChanged(sender As Object, e As EventArgs)
            Bind()
        End Sub

        Protected Sub gv_RowCommand(sender As Object, e As GridViewCommandEventArgs)
            If e.CommandName = "DeleteClient" Then
                ClientRepository.Delete(Convert.ToString(e.CommandArgument))
                Bind()
            End If
        End Sub

    End Class

End Namespace
