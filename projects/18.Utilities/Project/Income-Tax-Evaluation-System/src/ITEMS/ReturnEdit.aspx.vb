' =============================================================================
' Income Tax Evaluation System · ReturnEdit.aspx.vb — file / edit a return with server-side tax calc
' Enforces the SRS rule: a revised return needs an existing original one.
' =============================================================================
Imports System.Globalization
Imports System.Linq
Imports ITEMS.Logic
Imports ITEMS.Models
Imports ITEMS.Repositories
Imports System.Web.UI
Imports System.Web.UI.WebControls

Namespace ITEMS

    Partial Public Class ReturnEditPage
        Inherits System.Web.UI.Page

        Private ReadOnly inr As CultureInfo = CultureInfo.GetCultureInfo("en-IN")

        Private ReadOnly Property IsEdit As Boolean
            Get
                Return Not String.IsNullOrEmpty(Request.QueryString("pan"))
            End Get
        End Property

        Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
            litTitle.Text = If(IsEdit, "Edit", "File")
            If IsPostBack Then Return

            ddlClient.DataSource = ClientRepository.GetAll().
                Select(Function(c) New With {.Pan = c.Pan, .Display = c.Name & " — " & c.Pan}).ToList()
            ddlClient.DataBind()

            If IsEdit Then
                Dim rec = ReturnRepository.Get(Request.QueryString("pan"),
                                               Date.Parse(Request.QueryString("a1")),
                                               Date.Parse(Request.QueryString("a2")),
                                               Integer.Parse(Request.QueryString("t")))
                If rec Is Nothing Then Response.Redirect("Returns.aspx") : Return
                LoadRecord(rec)
                ddlClient.Enabled = False : txtAy1.ReadOnly = True : txtAy2.ReadOnly = True : ddlType.Enabled = False
            Else
                txtAy1.Text = ConfigDefault("AssessmentYearDefaultFrom", "2024-04-01")
                txtAy2.Text = ConfigDefault("AssessmentYearDefaultTo", "2025-03-31")
            End If
            RenderComputation(ReadForm())
        End Sub

        Private Shared Function ConfigDefault(key As String, fallback As String) As String
            Return If(System.Configuration.ConfigurationManager.AppSettings(key), fallback)
        End Function

        Private Sub LoadRecord(r As ReturnRecord)
            ddlClient.SelectedValue = r.Pan
            ddlType.SelectedValue = r.ReturnType.ToString()
            txtAy1.Text = r.AyFrom.ToString("yyyy-MM-dd") : txtAy2.Text = r.AyTo.ToString("yyyy-MM-dd")
            txtSalary.Text = Str(r.IncomeFromSalary) : txtHouse.Text = Str(r.IncomeFromHouseProperty)
            txtBusiness.Text = Str(r.IncomeFromBusiness) : txtStcg.Text = Str(r.ShortTermGain)
            txtLtcg.Text = Str(r.LongTermGain) : txtOther.Text = Str(r.IncomeFromOtherSources)
            txtClub.Text = Str(r.OtherPersonIncome) : txtVia.Text = Str(r.DeductionUnderVIA)
            txtTds.Text = Str(r.TdsAtSource) : txtAdvance.Text = Str(r.AdvanceTaxPaid)
            txtSelf.Text = Str(r.SelfAssessmentPaid) : txtInterest.Text = Str(r.InterestPayable)
            txtRelief.Text = Str(r.Relief)
        End Sub

        Private Shared Function Str(d As Decimal) As String
            Return If(d = 0D, "", d.ToString())
        End Function

        Private Function Num(t As TextBox) As Decimal
            Dim v As Decimal
            Return If(Decimal.TryParse(t.Text, v), v, 0D)
        End Function

        Private Function ReadForm() As ReturnRecord
            Return New ReturnRecord With {
                .Pan = ddlClient.SelectedValue, .ReturnType = Integer.Parse(ddlType.SelectedValue),
                .AyFrom = SafeDate(txtAy1.Text), .AyTo = SafeDate(txtAy2.Text),
                .IncomeFromSalary = Num(txtSalary), .IncomeFromHouseProperty = Num(txtHouse),
                .IncomeFromBusiness = Num(txtBusiness), .ShortTermGain = Num(txtStcg),
                .LongTermGain = Num(txtLtcg), .IncomeFromOtherSources = Num(txtOther),
                .OtherPersonIncome = Num(txtClub), .DeductionUnderVIA = Num(txtVia),
                .TdsAtSource = Num(txtTds), .AdvanceTaxPaid = Num(txtAdvance),
                .SelfAssessmentPaid = Num(txtSelf), .InterestPayable = Num(txtInterest), .Relief = Num(txtRelief)}
        End Function

        Private Shared Function SafeDate(s As String) As Date
            Dim d As Date
            Return If(Date.TryParse(s, d), d, Date.Today)
        End Function

        Private Function IsFirm() As Boolean
            Dim c = ClientRepository.Get(ddlClient.SelectedValue)
            Return c IsNot Nothing AndAlso c.IsFirm
        End Function

        Private Sub RenderComputation(rec As ReturnRecord)
            Dim firm = IsFirm()
            litRegime.Text = If(firm, "Firm @ 30%", "Old regime")
            Dim t = TaxEngine.Compute(rec, firm)
            Dim sb As New System.Text.StringBuilder()
            sb.Append(Line("Gross Total Income", t.GrossTotalIncome))
            sb.Append(Line("Less: Deductions VI-A", rec.DeductionUnderVIA))
            sb.Append(Line("Total Income", t.TotalIncome, True))
            sb.Append("<div style='height:.5rem'></div>")
            sb.Append(Line("Tax at normal rates", t.TaxAtNormalRate))
            sb.Append(Line("Tax at special rates", t.TaxAtSpecialRate))
            sb.Append(Line("Tax on Total Income", t.TaxOnTotalIncome))
            sb.Append(Line("Less: Rebate u/s 87A", t.Rebate87A))
            sb.Append(Line("Add: Surcharge", t.Surcharge))
            sb.Append(Line("Add: Health & Edu Cess (4%)", t.Cess))
            sb.Append(Line("Total Tax Payable", t.TotalTaxPayable, True))
            sb.Append(Line("Net Tax Payable", t.NetTaxPayable, True))
            Dim bal = t.BalancePayableOrRefund
            sb.Append($"<div class='total' style='border-top:2px dashed var(--line);margin-top:.6rem'><span>{If(bal < 0, "Refund Due", "Balance Payable")}</span><span>{Money(Math.Abs(bal))}</span></div>")
            litComp.Text = sb.ToString()
        End Sub

        Private Function Line(label As String, val As Decimal, Optional strong As Boolean = False) As String
            Return $"<div class='lrow' style='{If(strong, "font-weight:800;", "")}'><span>{label}</span><span class='amt'>{Money(val)}</span></div>"
        End Function

        Private Function Money(v As Decimal) As String
            Return v.ToString("C0", inr)
        End Function

        Protected Sub btnCompute_Click(sender As Object, e As EventArgs)
            RenderComputation(ReadForm())
        End Sub

        Protected Sub btnSave_Click(sender As Object, e As EventArgs)
            If Not Page.IsValid Then Return
            Dim rec = ReadForm()

            If Not IsEdit AndAlso rec.ReturnType = 1 AndAlso Not ReturnRepository.HasOriginal(rec.Pan, rec.AyFrom, rec.AyTo) Then
                litErr.Text = "An original return must be filed before a revised one (per SRS rule)."
                RenderComputation(rec)
                Return
            End If

            ReturnRepository.Save(rec, IsFirm(), Not IsEdit)
            Response.Redirect("Returns.aspx")
        End Sub

    End Class

End Namespace
