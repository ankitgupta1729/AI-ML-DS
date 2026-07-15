<%@ Page Language="VB" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="Returns.aspx.vb" Inherits="ITEMS.ReturnsPage" %>
<asp:Content ContentPlaceHolderID="Crumb" runat="server">Return Filing</asp:Content>
<asp:Content ContentPlaceHolderID="Main" runat="server">
  <div class="page-head"><div><h2>Return Filing</h2>
    <p class="muted">File original returns, revise mistakes, and let the engine compute the tax.</p></div>
    <a class="btn btn-primary" href="ReturnEdit.aspx">+ File New Return</a></div>
  <div class="card"><div class="table-wrap">
    <asp:GridView ID="gv" runat="server" CssClass="data" AutoGenerateColumns="false" GridLines="None"
      OnRowCommand="gv_RowCommand" EmptyDataText="No returns filed yet.">
      <Columns>
        <asp:BoundField DataField="PAN" HeaderText="PAN" ItemStyle-CssClass="mono" />
        <asp:BoundField DataField="CLIENT_NAME" HeaderText="Client" />
        <asp:BoundField DataField="ASSESSMENT_YEAR" HeaderText="AY" />
        <asp:BoundField DataField="RETURN_TYPE" HeaderText="Type" />
        <asp:BoundField DataField="TOTAL_INCOME" HeaderText="Total Income" DataFormatString="{0:C0}" ItemStyle-CssClass="num mono" />
        <asp:BoundField DataField="NET_TAX_PAYABLE" HeaderText="Net Tax" DataFormatString="{0:C0}" ItemStyle-CssClass="num mono" />
        <asp:TemplateField HeaderText="Actions">
          <ItemTemplate>
            <a class="btn btn-sm btn-ghost" href='ReturnEdit.aspx?pan=<%# Eval("PAN") %>&a1=<%# Eval("ASSES_YEAR_1","{0:yyyy-MM-dd}") %>&a2=<%# Eval("ASSES_YEAR_2","{0:yyyy-MM-dd}") %>&t=<%# Eval("RETURN_ORIGINAL_REVISED") %>'>Edit</a>
            <asp:LinkButton runat="server" CssClass="btn btn-sm btn-danger" CommandName="DeleteReturn"
              CommandArgument='<%# Eval("PAN") & "|" & Eval("ASSES_YEAR_1","{0:yyyy-MM-dd}") & "|" & Eval("ASSES_YEAR_2","{0:yyyy-MM-dd}") & "|" & Eval("RETURN_ORIGINAL_REVISED") %>'
              Text="Delete" OnClientClick="return confirm('Delete this return?');" />
          </ItemTemplate>
        </asp:TemplateField>
      </Columns>
    </asp:GridView>
  </div></div>
</asp:Content>
