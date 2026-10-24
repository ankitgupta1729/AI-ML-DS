<%@ Page Language="VB" MasterPageFile="~/Site.Master" AutoEventWireup="false" CodeBehind="ClientEdit.aspx.vb" Inherits="ITEMS.ClientEditPage" %>
<asp:Content ContentPlaceHolderID="Crumb" runat="server">Client Information / <asp:Literal ID="litMode" runat="server" /></asp:Content>
<asp:Content ContentPlaceHolderID="Main" runat="server">
  <div class="page-head"><div><h2><asp:Literal ID="litTitle" runat="server" /> Client Record</h2>
    <p class="muted">Enter the basic information of the client.</p></div>
    <a class="btn btn-ghost" href="Clients.aspx">← Back to list</a></div>
  <div class="card"><div class="card-body"><div class="form-grid">
    <div class="section-title">Identification</div>
    <div class="field"><label>PAN <span class="req">*</span></label>
      <asp:TextBox ID="txtPan" runat="server" MaxLength="10" placeholder="ABCDE1234F" Style="text-transform:uppercase" />
      <asp:RegularExpressionValidator runat="server" ControlToValidate="txtPan" CssClass="err-text" Display="Dynamic"
        ValidationExpression="^[A-Za-z]{5}[0-9]{4}[A-Za-z]$" ErrorMessage="PAN must match ABCDE1234F." /></div>
    <div class="field"><label>Full Name <span class="req">*</span></label>
      <asp:TextBox ID="txtName" runat="server" MaxLength="30" />
      <asp:RequiredFieldValidator runat="server" ControlToValidate="txtName" CssClass="err-text" Display="Dynamic" ErrorMessage="Name is required." /></div>
    <div class="field"><label>Father's Name</label><asp:TextBox ID="txtFather" runat="server" MaxLength="30" /></div>
    <div class="field"><label>Date of Birth</label><asp:TextBox ID="txtDob" runat="server" TextMode="Date" /></div>
    <div class="section-title">Contact</div>
    <div class="field full"><label>Address</label><asp:TextBox ID="txtAddr" runat="server" TextMode="MultiLine" MaxLength="60" /></div>
    <div class="field"><label>PIN Code</label>
      <asp:TextBox ID="txtPin" runat="server" MaxLength="6" />
      <asp:RegularExpressionValidator runat="server" ControlToValidate="txtPin" CssClass="err-text" Display="Dynamic"
        ValidationExpression="^[0-9]{6}$" ErrorMessage="PIN must be 6 digits." /></div>
    <div class="field"><label>Telephone</label><asp:TextBox ID="txtTel" runat="server" MaxLength="15" /></div>
    <div class="section-title">Classification</div>
    <div class="field"><label>Category</label>
      <asp:DropDownList ID="ddlCat" runat="server">
        <asp:ListItem Value="0">Individual</asp:ListItem><asp:ListItem Value="1">HUF</asp:ListItem>
        <asp:ListItem Value="2">Firm</asp:ListItem><asp:ListItem Value="3">AOP</asp:ListItem>
        <asp:ListItem Value="4">Local Authority</asp:ListItem></asp:DropDownList></div>
    <div class="field"><label>Residential Status</label>
      <asp:DropDownList ID="ddlRes" runat="server">
        <asp:ListItem Value="0">Resident</asp:ListItem><asp:ListItem Value="1">Non Resident</asp:ListItem>
        <asp:ListItem Value="2">Not Ordinarily Resident</asp:ListItem></asp:DropDownList></div>
    <div class="field"><label>Sex</label>
      <asp:DropDownList ID="ddlSex" runat="server">
        <asp:ListItem Value="1">Male</asp:ListItem><asp:ListItem Value="0">Female</asp:ListItem></asp:DropDownList></div>
    <div class="field"><label>Ward / Circle / Special Range</label><asp:TextBox ID="txtWard" runat="server" MaxLength="20" /></div>
  </div>
  <div class="err-text"><asp:Literal ID="litErr" runat="server" /></div>
  <div class="btn-row" style="margin-top:1rem">
    <asp:Button ID="btnSave" runat="server" CssClass="btn btn-primary" Text="💾 Save Client" OnClick="btnSave_Click" />
    <a class="btn btn-ghost" href="Clients.aspx">Cancel</a></div>
  </div></div>
</asp:Content>
