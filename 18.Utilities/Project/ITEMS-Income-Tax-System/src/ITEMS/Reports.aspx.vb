' =============================================================================
' ITEMS · Reports.aspx.vb — the four statutory reports (Report Generation module)
' =============================================================================
Imports System.Linq
Imports ITEMS.Data
Imports ITEMS.Repositories

Namespace ITEMS

    Partial Public Class ReportsPage
        Inherits System.Web.UI.Page

        Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
            If IsPostBack Then Return

            Dim clients = ClientRepository.GetAll().
                Select(Function(c) New With {.Pan = c.Pan, .Display = c.Name & " (" & c.Pan & ")"}).ToList()
            ddlR1.DataSource = clients : ddlR1.DataBind()
            ddlR3.DataSource = clients : ddlR3.DataBind()

            Dim fiscals = OracleDb.Query(
                "SELECT DISTINCT TO_CHAR(ASSES_YEAR_1,'YYYY-MM-DD') AS AY1, " &
                "TO_CHAR(ASSES_YEAR_1,'YYYY')||'-'||TO_CHAR(ASSES_YEAR_2,'YY') AS LABEL " &
                "FROM INCOME_TAX_RECORD ORDER BY 1")
            ddlR2.DataTextField = "LABEL" : ddlR2.DataValueField = "AY1"
            ddlR2.DataSource = fiscals : ddlR2.DataBind()
        End Sub

        Private Sub Show(title As String, dt As Data.DataTable)
            litTitle.Text = $"<h3>{Server.HtmlEncode(title)}</h3>"
            gvReport.DataSource = dt
            gvReport.DataBind()
        End Sub

        Protected Sub btnR1_Click(sender As Object, e As EventArgs)
            Show("Return History — " & ddlR1.SelectedItem.Text, ReturnRepository.ReturnHistory(ddlR1.SelectedValue))
        End Sub

        Protected Sub btnR2_Click(sender As Object, e As EventArgs)
            Show("All Returns filed in " & ddlR2.SelectedItem.Text, ReturnRepository.ReturnsInFiscal(Date.Parse(ddlR2.SelectedValue)))
        End Sub

        Protected Sub btnR3_Click(sender As Object, e As EventArgs)
            Show("Revised Returns — " & ddlR3.SelectedItem.Text, ReturnRepository.RevisedByClient(ddlR3.SelectedValue))
        End Sub

    End Class

End Namespace
