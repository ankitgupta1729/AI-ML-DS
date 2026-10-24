' =============================================================================
' Income Tax Evaluation System · Default.aspx.vb — dashboard KPIs and recent returns
' =============================================================================
Imports System.Globalization
Imports ITEMS.Data
Imports ITEMS.Repositories
Imports System.Web.UI
Imports System.Web.UI.WebControls

Namespace ITEMS

    Partial Public Class DefaultPage
        Inherits System.Web.UI.Page

        Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
            If IsPostBack Then Return

            Dim clients = ClientRepository.GetAll()
            Dim returns = ReturnRepository.GetAll()
            Dim firms = clients.FindAll(Function(c) c.IsFirm).Count
            Dim revised = returns.FindAll(Function(r) r.ReturnType = 1).Count
            Dim inr = CultureInfo.GetCultureInfo("en-IN")

            litClients.Text = clients.Count.ToString()
            litFirms.Text = $"{firms} firm(s) · {clients.Count - firms} individual(s)"
            litReturns.Text = returns.Count.ToString()
            litOrigRev.Text = $"{returns.Count - revised} original · {revised} revised"
            litRevised.Text = revised.ToString()

            Dim totalTax As Decimal = 0
            For Each r In returns : totalTax += r.NetTaxPayable : Next
            litTax.Text = totalTax.ToString("C0", inr)

            gvRecent.DataSource = OracleDb.Query(
                "SELECT * FROM (SELECT c.CLIENT_NAME, " &
                "TO_CHAR(r.ASSES_YEAR_1,'YYYY')||'-'||TO_CHAR(r.ASSES_YEAR_2,'YY') AS ASSESSMENT_YEAR, " &
                "CASE r.RETURN_ORIGINAL_REVISED WHEN 1 THEN 'Revised' ELSE 'Original' END AS RETURN_TYPE, " &
                "r.TOTAL_INCOME, r.NET_TAX_PAYABLE " &
                "FROM INCOME_TAX_RECORD r JOIN CLIENT_RECORD c ON c.PAN=r.PAN " &
                "ORDER BY r.ASSES_YEAR_1 DESC) WHERE ROWNUM <= 6")
            gvRecent.DataBind()
        End Sub

    End Class

End Namespace
