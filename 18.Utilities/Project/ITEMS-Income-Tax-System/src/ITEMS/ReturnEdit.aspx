<%@ Page Language="VB" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="ReturnEdit.aspx.vb" Inherits="ITEMS.ReturnEditPage" %>
<asp:Content ContentPlaceHolderID="Crumb" runat="server">Return Filing / File Return</asp:Content>
<asp:Content ContentPlaceHolderID="Main" runat="server">
  <div class="page-head"><div><h2><asp:Literal ID="litTitle" runat="server" /> Income Tax Return</h2>
    <p class="muted">Verify the client, enter income heads, then Compute to see the tax liability.</p></div>
    <a class="btn btn-ghost" href="Returns.aspx">← Back</a></div>
  <div class="grid" style="grid-template-columns:1.6fr 1fr;gap:1.1rem">
    <div class="card"><div class="card-body"><div class="form-grid">
      <div class="section-title">Return header</div>
      <div class="field"><label>Client (PAN) <span class="req">*</span></label>
        <asp:DropDownList ID="ddlClient" runat="server" DataTextField="Display" DataValueField="Pan" /></div>
      <div class="field"><label>Return Type</label>
        <asp:DropDownList ID="ddlType" runat="server">
          <asp:ListItem Value="0">Original</asp:ListItem><asp:ListItem Value="1">Revised</asp:ListItem></asp:DropDownList></div>
      <div class="field"><label>Assessment Year — From</label><asp:TextBox ID="txtAy1" runat="server" TextMode="Date" /></div>
      <div class="field"><label>Assessment Year — To</label><asp:TextBox ID="txtAy2" runat="server" TextMode="Date" /></div>
      <div class="section-title">Income heads</div>
      <div class="field"><label>Income from Salary</label><asp:TextBox ID="txtSalary" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Income from House Property</label><asp:TextBox ID="txtHouse" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Income from Business / Profession</label><asp:TextBox ID="txtBusiness" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Short-term Capital Gain</label><asp:TextBox ID="txtStcg" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Long-term Capital Gain</label><asp:TextBox ID="txtLtcg" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Income from Other Sources</label><asp:TextBox ID="txtOther" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Income of Other Person (clubbed)</label><asp:TextBox ID="txtClub" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Less: Deductions (Chapter VI-A)</label><asp:TextBox ID="txtVia" runat="server" TextMode="Number" /></div>
      <div class="section-title">Taxes already paid</div>
      <div class="field"><label>Tax Deducted at Source</label><asp:TextBox ID="txtTds" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Advance Tax Paid</label><asp:TextBox ID="txtAdvance" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Self-Assessment Tax Paid</label><asp:TextBox ID="txtSelf" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Interest Payable</label><asp:TextBox ID="txtInterest" runat="server" TextMode="Number" /></div>
      <div class="field"><label>Less: Relief</label><asp:TextBox ID="txtRelief" runat="server" TextMode="Number" /></div>
    </div>
    <div class="err-text"><asp:Literal ID="litErr" runat="server" /></div>
    <div class="btn-row" style="margin-top:1rem">
      <asp:Button ID="btnCompute" runat="server" CssClass="btn btn-ghost" Text="🧮 Compute" OnClick="btnCompute_Click" CausesValidation="false" />
      <asp:Button ID="btnSave" runat="server" CssClass="btn btn-primary" Text="💾 File Return" OnClick="btnSave_Click" />
      <a class="btn btn-ghost" href="Returns.aspx">Cancel</a></div>
    </div></div>
    <div><div class="card" style="position:sticky;top:76px"><div class="card-head"><h3>Computation of Tax</h3>
      <span class="pill"><asp:Literal ID="litRegime" runat="server">Old regime</asp:Literal></span></div>
      <div class="card-body"><asp:Literal ID="litComp" runat="server" /></div></div></div>
  </div>
</asp:Content>
