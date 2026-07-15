' =============================================================================
' ITEMS · FirmAccount.aspx.vb — one page drives Trading / P&L / Balance Sheet
' via ?m=trading|pl|balance, using FirmAccountRepository + FirmAccountSpec.
' =============================================================================
Imports System.Collections.Generic
Imports System.Data
Imports System.Globalization
Imports System.Linq
Imports ITEMS.Repositories

Namespace ITEMS

    Partial Public Class FirmAccountPage
        Inherits System.Web.UI.Page

        Private ReadOnly inr As CultureInfo = CultureInfo.GetCultureInfo("en-IN")

        Private ReadOnly Property ModuleKey As String
            Get
                Return If(Request.QueryString("m"), "trading")
            End Get
        End Property

        Private ReadOnly Property Spec As FirmAccountSpec
            Get
                Return FirmAccountRepository.GetSpec(ModuleKey)
            End Get
        End Property

        Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
            litTitle.Text = Spec.Title
            litCrumb.Text = Spec.Title
            litLeftHead.Text = Spec.LeftHead
            litRightHead.Text = Spec.RightHead
            ' Money inputs must be re-created on every postback for ViewState to bind.
            BuildInputs()
            If Not IsPostBack Then BindList()
        End Sub

        Private Sub BuildInputs()
            phLeft.Controls.Clear() : phRight.Controls.Clear()
            For Each c In Spec.LeftCols : phLeft.Controls.Add(FieldFor(c)) : Next
            For Each c In Spec.RightCols : phRight.Controls.Add(FieldFor(c)) : Next
        End Sub

        Private Function FieldFor(col As String) As Control
            Dim wrap As New HtmlGenericControl("div") With {.InnerHtml = ""}
            wrap.Attributes("class") = "field"
            wrap.Attributes("style") = "margin-bottom:.5rem"
            Dim lbl As New HtmlGenericControl("label") With {.InnerText = Humanize(col)}
            Dim tb As New TextBox With {.ID = "f_" & col, .CssClass = "money"}
            tb.Attributes("type") = "number"
            wrap.Controls.Add(lbl)
            wrap.Controls.Add(tb)
            Return wrap
        End Function

        Private Shared Function Humanize(k As String) As String
            Dim s = System.Text.RegularExpressions.Regex.Replace(k, "^TO_|^BY_", "").Replace("_", " ").ToLowerInvariant()
            Return CultureInfo.CurrentCulture.TextInfo.ToTitleCase(s)
        End Function

        Private Sub BindList()
            Dim dt = FirmAccountRepository.List(Spec)
            Dim view As New DataTable()
            view.Columns.Add("PAN") : view.Columns.Add("CLIENT_NAME") : view.Columns.Add("AY")
            view.Columns.Add("LEFT_TOTAL", GetType(Decimal)) : view.Columns.Add("RIGHT_TOTAL", GetType(Decimal))
            view.Columns.Add("STATUS") : view.Columns.Add("KEY")
            For Each r As DataRow In dt.Rows
                Dim lt = FirmAccountRepository.SideTotal(r, Spec.LeftCols)
                Dim rt = FirmAccountRepository.SideTotal(r, Spec.RightCols)
                Dim a1 = Convert.ToDateTime(r("ASSES_YEAR_1"))
                Dim a2 = Convert.ToDateTime(r("ASSES_YEAR_2"))
                view.Rows.Add(r("PAN"), r("CLIENT_NAME"), a1.ToString("yyyy") & "-" & a2.ToString("yy"),
                              lt, rt, If(Math.Abs(lt - rt) < 1, "Balanced", "Δ " & Math.Abs(lt - rt).ToString("C0", inr)),
                              r("PAN") & "|" & a1.ToString("yyyy-MM-dd") & "|" & a2.ToString("yyyy-MM-dd"))
            Next
            gv.DataSource = view : gv.DataBind()
        End Sub

        Protected Sub btnNew_Click(sender As Object, e As EventArgs)
            ddlFirm.DataSource = ClientRepository.GetFirms().
                Select(Function(c) New With {.Pan = c.Pan, .Display = c.Name & " — " & c.Pan}).ToList()
            ddlFirm.DataBind()
            txtA1.Text = "2024-04-01" : txtA2.Text = "2025-03-31"
            ClearInputs()
            pnlList.Visible = False : pnlForm.Visible = True
        End Sub

        Protected Sub gv_RowCommand(sender As Object, e As GridViewCommandEventArgs)
            Dim parts = Convert.ToString(e.CommandArgument).Split("|"c)
            Dim pan = parts(0), a1 = Date.Parse(parts(1)), a2 = Date.Parse(parts(2))
            If e.CommandName = "DelRec" Then
                FirmAccountRepository.Delete(Spec, pan, a1, a2)
                BindList()
            ElseIf e.CommandName = "EditRec" Then
                ddlFirm.DataSource = ClientRepository.GetFirms().
                    Select(Function(c) New With {.Pan = c.Pan, .Display = c.Name & " — " & c.Pan}).ToList()
                ddlFirm.DataBind()
                ddlFirm.SelectedValue = pan : ddlFirm.Enabled = False
                txtA1.Text = a1.ToString("yyyy-MM-dd") : txtA2.Text = a2.ToString("yyyy-MM-dd")
                Dim row = FirmAccountRepository.Get(Spec, pan, a1, a2)
                For Each col In Spec.AllCols
                    Dim tb = TryCast(FindControlRecursive(Me, "f_" & col), TextBox)
                    If tb IsNot Nothing AndAlso row.Table.Columns.Contains(col) AndAlso Not IsDBNull(row(col)) Then
                        Dim v = Convert.ToDecimal(row(col))
                        tb.Text = If(v = 0D, "", v.ToString())
                    End If
                Next
                pnlList.Visible = False : pnlForm.Visible = True
            End If
        End Sub

        Protected Sub btnSave_Click(sender As Object, e As EventArgs)
            Dim vals As New Dictionary(Of String, Decimal)
            For Each col In Spec.AllCols
                Dim tb = TryCast(FindControlRecursive(Me, "f_" & col), TextBox)
                Dim v As Decimal
                vals(col) = If(tb IsNot Nothing AndAlso Decimal.TryParse(tb.Text, v), v, 0D)
            Next
            Dim pan = ddlFirm.SelectedValue, a1 = Date.Parse(txtA1.Text), a2 = Date.Parse(txtA2.Text)
            Dim isNew = FirmAccountRepository.Get(Spec, pan, a1, a2) Is Nothing
            FirmAccountRepository.Save(Spec, pan, a1, a2, vals, isNew)
            pnlForm.Visible = False : pnlList.Visible = True
            BindList()
        End Sub

        Protected Sub btnCancel_Click(sender As Object, e As EventArgs)
            pnlForm.Visible = False : pnlList.Visible = True
        End Sub

        Private Sub ClearInputs()
            For Each col In Spec.AllCols
                Dim tb = TryCast(FindControlRecursive(Me, "f_" & col), TextBox)
                If tb IsNot Nothing Then tb.Text = ""
            Next
        End Sub

        Private Function FindControlRecursive(root As Control, id As String) As Control
            If root.ID = id Then Return root
            For Each c As Control In root.Controls
                Dim found = FindControlRecursive(c, id)
                If found IsNot Nothing Then Return found
            Next
            Return Nothing
        End Function

    End Class

End Namespace
