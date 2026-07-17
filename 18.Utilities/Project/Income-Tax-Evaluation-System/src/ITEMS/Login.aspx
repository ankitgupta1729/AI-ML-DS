<%@ Page Language="VB" AutoEventWireup="false" CodeBehind="Login.aspx.vb" Inherits="ITEMS.LoginPage" %>
<!DOCTYPE html>
<html lang="en">
<head runat="server">
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Sign in · Income Tax Evaluation System</title>
  <link rel="stylesheet" href="<%= ResolveUrl("~/Content/site.css") %>" />
</head>
<body>
  <form id="form1" runat="server">
    <div class="login-wrap"><div class="login-card">
      <div class="login-head">
        <div class="logo"><span class="mark">₹</span> Income Tax Evaluation System</div>
        <h1>Sign in to your workspace</h1>
        <p>Client records · Return filing · Firm accounts · Reports</p>
      </div>
      <div class="login-body">
        <div class="field"><label>User ID <span class="req">*</span></label>
          <asp:TextBox ID="txtUser" runat="server" placeholder="e.g. admin" />
        </div>
        <div class="field"><label>Password <span class="req">*</span></label>
          <asp:TextBox ID="txtPass" runat="server" TextMode="Password" placeholder="Enter password" />
        </div>
        <div class="err-text"><asp:Literal ID="litErr" runat="server" /></div>
        <asp:Button ID="btnLogin" runat="server" CssClass="btn btn-primary" Style="width:100%"
          Text="Sign in →" OnClick="btnLogin_Click" />
        <div class="hint">Demo credentials — Admin: <code>admin</code> / <code>admin@123</code> ·
          Operator: <code>operator</code> / <code>demo@2025</code></div>
      </div>
    </div></div>
  </form>
</body>
</html>
