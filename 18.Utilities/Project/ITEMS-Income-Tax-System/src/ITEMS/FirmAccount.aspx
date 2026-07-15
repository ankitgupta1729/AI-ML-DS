<%@ Page Language="VB" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="FirmAccount.aspx.vb" Inherits="ITEMS.FirmAccountPage" %>
<asp:Content ContentPlaceHolderID="Crumb" runat="server"><asp:Literal ID="litCrumb" runat="server" /></asp:Content>
<asp:Content ContentPlaceHolderID="Main" runat="server">
  <div class="page-head"><div><h2><asp:Literal ID="litTitle" runat="server" /></h2>
    <p class="muted">Firm accounts — both sides are totalled and checked for balance.</p></div>
    <asp:Button ID="btnNew" runat="server" CssClass="btn btn-primary" Text="+ New record" OnClick="btnNew_Click" CausesValidation="false" /></div>

  <asp:Panel ID="pnlList" runat="server">
    <div class="card"><div class="table-wrap">
      <asp:GridView ID="gv" runat="server" CssClass="data" AutoGenerateColumns="false" GridLines="None"
        OnRowCommand="gv_RowCommand" EmptyDataText="No records yet. Only Firm-category clients can have these accounts.">
        <Columns>
          <asp:BoundField DataField="PAN" HeaderText="PAN" ItemStyle-CssClass="mono" />
          <asp:BoundField DataField="CLIENT_NAME" HeaderText="Firm" />
          <asp:BoundField DataField="AY" HeaderText="AY" />
          <asp:BoundField DataField="LEFT_TOTAL" HeaderText="Left Total" DataFormatString="{0:C0}" ItemStyle-CssClass="num mono" />
          <asp:BoundField DataField="RIGHT_TOTAL" HeaderText="Right Total" DataFormatString="{0:C0}" ItemStyle-CssClass="num mono" />
          <asp:BoundField DataField="STATUS" HeaderText="Status" />
          <asp:TemplateField HeaderText="Actions"><ItemTemplate>
            <asp:LinkButton runat="server" CssClass="btn btn-sm btn-ghost" CommandName="EditRec"
              CommandArgument='<%# Eval("KEY") %>' Text="Edit" />
            <asp:LinkButton runat="server" CssClass="btn btn-sm btn-danger" CommandName="DelRec"
              CommandArgument='<%# Eval("KEY") %>' Text="Delete" OnClientClick="return confirm('Delete this record?');" />
          </ItemTemplate></asp:TemplateField>
        </Columns>
      </asp:GridView>
    </div></div>
  </asp:Panel>

  <asp:Panel ID="pnlForm" runat="server" Visible="false">
    <div class="card"><div class="card-body">
      <div class="form-grid" style="margin-bottom:.5rem">
        <div class="field"><label>Firm (PAN)</label><asp:DropDownList ID="ddlFirm" runat="server" DataTextField="Display" DataValueField="Pan" /></div>
        <div class="field"><label>AY From</label><asp:TextBox ID="txtA1" runat="server" TextMode="Date" /></div>
        <div class="field"><label>AY To</label><asp:TextBox ID="txtA2" runat="server" TextMode="Date" /></div>
      </div>
      <div class="ledger">
        <div class="side"><h4><asp:Literal ID="litLeftHead" runat="server" /></h4>
          <asp:PlaceHolder ID="phLeft" runat="server" /></div>
        <div class="side"><h4><asp:Literal ID="litRightHead" runat="server" /></h4>
          <asp:PlaceHolder ID="phRight" runat="server" /></div>
      </div>
      <div class="btn-row" style="margin-top:1rem">
        <asp:Button ID="btnSave" runat="server" CssClass="btn btn-primary" Text="💾 Save" OnClick="btnSave_Click" />
        <asp:Button ID="btnCancel" runat="server" CssClass="btn btn-ghost" Text="Cancel" OnClick="btnCancel_Click" CausesValidation="false" />
      </div>
    </div></div>
  </asp:Panel>
</asp:Content>
