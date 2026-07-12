Partial Class MainForm
    Friend WithEvents lblUser As System.Windows.Forms.Label
    Friend WithEvents btnClients As System.Windows.Forms.Button
    Friend WithEvents btnTax As System.Windows.Forms.Button
    Friend WithEvents btnTrading As System.Windows.Forms.Button
    Friend WithEvents btnPL As System.Windows.Forms.Button
    Friend WithEvents btnBS As System.Windows.Forms.Button
    Friend WithEvents btnReports As System.Windows.Forms.Button
    Friend WithEvents btnLogout As System.Windows.Forms.Button

    Private Sub InitializeComponent()
        Me.lblUser = New System.Windows.Forms.Label()
        Me.btnClients = New System.Windows.Forms.Button()
        Me.btnTax = New System.Windows.Forms.Button()
        Me.btnTrading = New System.Windows.Forms.Button()
        Me.btnPL = New System.Windows.Forms.Button()
        Me.btnBS = New System.Windows.Forms.Button()
        Me.btnReports = New System.Windows.Forms.Button()
        Me.btnLogout = New System.Windows.Forms.Button()
        Me.SuspendLayout()
        '
        'lblUser
        '
        Me.lblUser.AutoSize = True
        Me.lblUser.Location = New System.Drawing.Point(12, 15)
        Me.lblUser.Name = "lblUser"
        Me.lblUser.Size = New System.Drawing.Size(48, 13)
        Me.lblUser.TabIndex = 0
        Me.lblUser.Text = "Welcome"
        '
        'btnClients
        '
        Me.btnClients.Location = New System.Drawing.Point(12, 40)
        Me.btnClients.Name = "btnClients"
        Me.btnClients.Size = New System.Drawing.Size(120, 30)
        Me.btnClients.TabIndex = 1
        Me.btnClients.Text = "Clients"
        Me.btnClients.UseVisualStyleBackColor = True
        '
        'btnTax
        '
        Me.btnTax.Location = New System.Drawing.Point(138, 40)
        Me.btnTax.Name = "btnTax"
        Me.btnTax.Size = New System.Drawing.Size(120, 30)
        Me.btnTax.TabIndex = 2
        Me.btnTax.Text = "Income Tax"
        Me.btnTax.UseVisualStyleBackColor = True
        '
        'btnTrading
        '
        Me.btnTrading.Location = New System.Drawing.Point(264, 40)
        Me.btnTrading.Name = "btnTrading"
        Me.btnTrading.Size = New System.Drawing.Size(120, 30)
        Me.btnTrading.TabIndex = 3
        Me.btnTrading.Text = "Trading"
        Me.btnTrading.UseVisualStyleBackColor = True
        '
        'btnPL
        '
        Me.btnPL.Location = New System.Drawing.Point(12, 76)
        Me.btnPL.Name = "btnPL"
        Me.btnPL.Size = New System.Drawing.Size(120, 30)
        Me.btnPL.TabIndex = 4
        Me.btnPL.Text = "P&L Account"
        Me.btnPL.UseVisualStyleBackColor = True
        '
        'btnBS
        '
        Me.btnBS.Location = New System.Drawing.Point(138, 76)
        Me.btnBS.Name = "btnBS"
        Me.btnBS.Size = New System.Drawing.Size(120, 30)
        Me.btnBS.TabIndex = 5
        Me.btnBS.Text = "Balance Sheet"
        Me.btnBS.UseVisualStyleBackColor = True
        '
        'btnReports
        '
        Me.btnReports.Location = New System.Drawing.Point(264, 76)
        Me.btnReports.Name = "btnReports"
        Me.btnReports.Size = New System.Drawing.Size(120, 30)
        Me.btnReports.TabIndex = 6
        Me.btnReports.Text = "Reports"
        Me.btnReports.UseVisualStyleBackColor = True
        '
        'btnLogout
        '
        Me.btnLogout.Location = New System.Drawing.Point(264, 12)
        Me.btnLogout.Name = "btnLogout"
        Me.btnLogout.Size = New System.Drawing.Size(120, 23)
        Me.btnLogout.TabIndex = 7
        Me.btnLogout.Text = "Logout"
        Me.btnLogout.UseVisualStyleBackColor = True
        '
        'MainForm
        '
        Me.AcceptButton = Me.btnClients
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(396, 118)
        Me.Controls.Add(Me.btnLogout)
        Me.Controls.Add(Me.btnReports)
        Me.Controls.Add(Me.btnBS)
        Me.Controls.Add(Me.btnPL)
        Me.Controls.Add(Me.btnTrading)
        Me.Controls.Add(Me.btnTax)
        Me.Controls.Add(Me.btnClients)
        Me.Controls.Add(Me.lblUser)
        Me.Name = "MainForm"
        Me.Text = "Income Tax Evaluation System"
        Me.ResumeLayout(False)
        Me.PerformLayout()
    End Sub
End Class
