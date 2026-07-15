' =============================================================================
' ITEMS · ClientEdit.aspx.vb — insert / update a client
' =============================================================================
Imports ITEMS.Models
Imports ITEMS.Repositories

Namespace ITEMS

    Partial Public Class ClientEditPage
        Inherits System.Web.UI.Page

        Private ReadOnly Property EditPan As String
            Get
                Return Request.QueryString("pan")
            End Get
        End Property

        Private ReadOnly Property IsEdit As Boolean
            Get
                Return Not String.IsNullOrEmpty(EditPan)
            End Get
        End Property

        Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
            litTitle.Text = If(IsEdit, "Update", "Insert")
            litMode.Text = If(IsEdit, "Update", "Insert")
            If IsPostBack Then Return

            If IsEdit Then
                Dim c = ClientRepository.Get(EditPan)
                If c Is Nothing Then Response.Redirect("Clients.aspx") : Return
                txtPan.Text = c.Pan : txtPan.ReadOnly = True
                txtName.Text = c.Name : txtFather.Text = c.FathersName
                If c.Dob.HasValue Then txtDob.Text = c.Dob.Value.ToString("yyyy-MM-dd")
                txtAddr.Text = c.Address : txtPin.Text = c.Pincode : txtTel.Text = c.Telephone
                txtWard.Text = c.WardCircleRange
                ddlCat.SelectedValue = c.Category.ToString()
                ddlRes.SelectedValue = c.Residence.ToString()
                ddlSex.SelectedValue = c.Sex.ToString()
            End If
        End Sub

        Protected Sub btnSave_Click(sender As Object, e As EventArgs)
            If Not Page.IsValid Then Return
            Dim pan = txtPan.Text.Trim().ToUpperInvariant()

            If Not IsEdit AndAlso ClientRepository.Exists(pan) Then
                litErr.Text = "A client with this PAN already exists."
                Return
            End If

            Dim c As New Client With {
                .Pan = pan, .Name = txtName.Text.Trim(), .FathersName = txtFather.Text.Trim(),
                .Dob = If(String.IsNullOrEmpty(txtDob.Text), CType(Nothing, Date?), Date.Parse(txtDob.Text)),
                .Pincode = txtPin.Text.Trim(), .Address = txtAddr.Text.Trim(), .Telephone = txtTel.Text.Trim(),
                .Category = Integer.Parse(ddlCat.SelectedValue), .Residence = Integer.Parse(ddlRes.SelectedValue),
                .Sex = Integer.Parse(ddlSex.SelectedValue), .WardCircleRange = txtWard.Text.Trim()}

            If IsEdit Then ClientRepository.Update(c) Else ClientRepository.Insert(c)
            Response.Redirect("Clients.aspx")
        End Sub

    End Class

End Namespace
