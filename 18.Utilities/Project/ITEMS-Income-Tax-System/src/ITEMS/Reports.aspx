<%@ Page Language="VB" MasterPageFile="~/Site.Master" AutoEventWireup="false" CodeBehind="Reports.aspx.vb" Inherits="ITEMS.ReportsPage" %>
<asp:Content ContentPlaceHolderID="Crumb" runat="server">Reports</asp:Content>
<asp:Content ContentPlaceHolderID="Main" runat="server">
  <div class="page-head"><div><h2>Report Generation</h2>
    <p class="muted">Generate the four statutory reports defined in the SRS.</p></div></div>
  <div class="grid grid-2">
    <div class="card"><div class="card-head"><h3>1 · Return history of a client</h3></div>
      <div class="card-body"><div class="field"><label>Select client</label>
        <asp:DropDownList ID="ddlR1" runat="server" DataTextField="Display" DataValueField="Pan" /></div>
        <asp:Button ID="btnR1" runat="server" CssClass="btn btn-primary" Text="Generate" OnClick="btnR1_Click" /></div></div>
    <div class="card"><div class="card-head"><h3>2 · Returns in a fiscal (all clients)</h3></div>
      <div class="card-body"><div class="field"><label>Fiscal (AY from)</label>
        <asp:DropDownList ID="ddlR2" runat="server" /></div>
        <asp:Button ID="btnR2" runat="server" CssClass="btn btn-primary" Text="Generate" OnClick="btnR2_Click" /></div></div>
    <div class="card"><div class="card-head"><h3>3 · Revised returns of a client</h3></div>
      <div class="card-body"><div class="field"><label>Select client</label>
        <asp:DropDownList ID="ddlR3" runat="server" DataTextField="Display" DataValueField="Pan" /></div>
        <asp:Button ID="btnR3" runat="server" CssClass="btn btn-primary" Text="Generate" OnClick="btnR3_Click" /></div></div>
    <div class="card"><div class="card-head"><h3>Print</h3></div>
      <div class="card-body"><p class="muted">Generate a report, then use your browser's Print (Ctrl/Cmd+P) to save it as PDF for the client file.</p>
        <button type="button" class="btn btn-accent" onclick="window.print()">🖨️ Print / Save PDF</button></div></div>
  </div>
  <div style="margin-top:1.4rem"><asp:Literal ID="litTitle" runat="server" />
    <asp:GridView ID="gvReport" runat="server" CssClass="data" GridLines="None" Style="margin-top:.6rem" /></div>
</asp:Content>
