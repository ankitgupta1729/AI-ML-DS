<%@ Page Language="VB" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="Default.aspx.vb" Inherits="ITEMS.DefaultPage" %>
<asp:Content ContentPlaceHolderID="Crumb" runat="server">Dashboard</asp:Content>
<asp:Content ContentPlaceHolderID="Main" runat="server">
  <div class="page-head"><div><h2>Welcome to ITEMS</h2>
    <p class="muted">A consolidated view of clients, returns and tax collections.</p></div>
    <div class="btn-row"><a class="btn btn-primary" href="ClientEdit.aspx">+ New client</a></div></div>
  <div class="grid grid-4" style="margin-bottom:1.2rem">
    <div class="stat i1"><div class="ico">👥</div><div class="lbl">Total Clients</div>
      <div class="val mono"><asp:Literal ID="litClients" runat="server" /></div>
      <div class="sub"><asp:Literal ID="litFirms" runat="server" /></div></div>
    <div class="stat i2"><div class="ico">📄</div><div class="lbl">Returns Filed</div>
      <div class="val mono"><asp:Literal ID="litReturns" runat="server" /></div>
      <div class="sub"><asp:Literal ID="litOrigRev" runat="server" /></div></div>
    <div class="stat i3"><div class="ico">🔁</div><div class="lbl">Revised Returns</div>
      <div class="val mono"><asp:Literal ID="litRevised" runat="server" /></div>
      <div class="sub">Corrections to original filings</div></div>
    <div class="stat i4"><div class="ico">💰</div><div class="lbl">Net Tax (recorded)</div>
      <div class="val mono"><asp:Literal ID="litTax" runat="server" /></div>
      <div class="sub">Across all assessment years</div></div>
  </div>
  <div class="card"><div class="card-head"><h3>Recent Returns</h3>
    <a class="btn btn-sm btn-ghost" href="Returns.aspx">All →</a></div>
    <div class="card-body" style="padding:0"><div class="table-wrap">
      <asp:GridView ID="gvRecent" runat="server" CssClass="data" AutoGenerateColumns="false" GridLines="None">
        <Columns>
          <asp:BoundField DataField="CLIENT_NAME" HeaderText="Client" />
          <asp:BoundField DataField="ASSESSMENT_YEAR" HeaderText="AY" />
          <asp:BoundField DataField="RETURN_TYPE" HeaderText="Type" />
          <asp:BoundField DataField="TOTAL_INCOME" HeaderText="Total Income" DataFormatString="{0:C0}" ItemStyle-CssClass="num mono" />
          <asp:BoundField DataField="NET_TAX_PAYABLE" HeaderText="Net Tax" DataFormatString="{0:C0}" ItemStyle-CssClass="num mono" />
        </Columns>
      </asp:GridView>
    </div></div></div>
</asp:Content>
