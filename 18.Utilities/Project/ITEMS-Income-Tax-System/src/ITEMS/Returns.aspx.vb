' =============================================================================
' ITEMS · Returns.aspx.vb — list & delete income-tax returns
' =============================================================================
Imports ITEMS.Data
Imports ITEMS.Repositories

Namespace ITEMS

    Partial Public Class ReturnsPage
        Inherits System.Web.UI.Page

        Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
            If Not IsPostBack Then Bind()
        End Sub

        Private Sub Bind()
            gv.DataSource = OracleDb.Query(
                "SELECT r.PAN, c.CLIENT_NAME, r.ASSES_YEAR_1, r.ASSES_YEAR_2, r.RETURN_ORIGINAL_REVISED, " &
                "TO_CHAR(r.ASSES_YEAR_1,'YYYY')||'-'||TO_CHAR(r.ASSES_YEAR_2,'YY') AS ASSESSMENT_YEAR, " &
                "CASE r.RETURN_ORIGINAL_REVISED WHEN 1 THEN 'Revised' ELSE 'Original' END AS RETURN_TYPE, " &
                "r.TOTAL_INCOME, r.NET_TAX_PAYABLE " &
                "FROM INCOME_TAX_RECORD r JOIN CLIENT_RECORD c ON c.PAN=r.PAN " &
                "ORDER BY r.ASSES_YEAR_1 DESC, c.CLIENT_NAME")
            gv.DataBind()
        End Sub

        Protected Sub gv_RowCommand(sender As Object, e As GridViewCommandEventArgs)
            If e.CommandName = "DeleteReturn" Then
                Dim parts = Convert.ToString(e.CommandArgument).Split("|"c)
                ReturnRepository.Delete(parts(0), Date.Parse(parts(1)), Date.Parse(parts(2)), Integer.Parse(parts(3)))
                Bind()
            End If
        End Sub

    End Class

End Namespace
