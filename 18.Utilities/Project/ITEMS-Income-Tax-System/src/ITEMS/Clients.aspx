<%@ Page Language="VB" MasterPageFile="~/Site.Master" AutoEventWireup="false" CodeBehind="Clients.aspx.vb" Inherits="ITEMS.ClientsPage" %>
<asp:Content ContentPlaceHolderID="Crumb" runat="server">Client Information</asp:Content>
<asp:Content ContentPlaceHolderID="Main" runat="server">
  <div class="page-head"><div><h2>Client Information</h2>
    <p class="muted">Add, update and remove clients. PAN is the unique primary key.</p></div>
    <a class="btn btn-primary" href="ClientEdit.aspx">+ Insert Client Record</a></div>
  <div class="toolbar">
    <div class="search" style="flex:1"><span class="mag">🔍</span>
      <asp:TextBox ID="txtSearch" runat="server" placeholder="Search by name, PAN or address..." AutoPostBack="true"
        OnTextChanged="txtSearch_TextChanged" Style="padding-left:2.2rem" /></div>
  </div>
  <div class="card"><div class="table-wrap">
    <asp:GridView ID="gv" runat="server" CssClass="data" AutoGenerateColumns="false" GridLines="None"
      DataKeyNames="PAN" OnRowCommand="gv_RowCommand" EmptyDataText="No clients found. Add your first client to begin.">
      <Columns>
        <asp:BoundField DataField="PAN" HeaderText="PAN" ItemStyle-CssClass="mono" />
        <asp:BoundField DataField="CLIENT_NAME" HeaderText="Name" />
        <asp:BoundField DataField="CATEGORY_TEXT" HeaderText="Category" />
        <asp:BoundField DataField="DOB" HeaderText="Date of Birth" DataFormatString="{0:dd-MMM-yyyy}" />
        <asp:BoundField DataField="WARD_CIRCLE_SPECIAL_RANGE" HeaderText="Ward/Circle" />
        <asp:TemplateField HeaderText="Actions">
          <ItemTemplate>
            <a class="btn btn-sm btn-ghost" href='ClientEdit.aspx?pan=<%# Eval("PAN") %>'>Edit</a>
            <asp:LinkButton runat="server" CssClass="btn btn-sm btn-danger" CommandName="DeleteClient"
              CommandArgument='<%# Eval("PAN") %>' Text="Delete"
              OnClientClick="return confirm('Delete this client and all linked returns/accounts?');" />
          </ItemTemplate>
        </asp:TemplateField>
      </Columns>
    </asp:GridView>
  </div></div>
</asp:Content>
