Partial Class PLAccountForm
    Friend WithEvents cmbClient As System.Windows.Forms.ComboBox
    Friend WithEvents txtAY As System.Windows.Forms.TextBox
    Friend WithEvents txtNetProfit As System.Windows.Forms.TextBox
    Friend WithEvents btnSave As System.Windows.Forms.Button

    Private Sub InitializeComponent()
        Me.cmbClient = New System.Windows.Forms.ComboBox()
        Me.txtAY = New System.Windows.Forms.TextBox()
        Me.txtNetProfit = New System.Windows.Forms.TextBox()
        Me.btnSave = New System.Windows.Forms.Button()
        Me.SuspendLayout()
        '
        'cmbClient
        '
        Me.cmbClient.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        Me.cmbClient.FormattingEnabled = True
        Me.cmbClient.Location = New System.Drawing.Point(12, 12)
        Me.cmbClient.Name = "cmbClient"
        Me.cmbClient.Size = New System.Drawing.Size(180, 21)
        Me.cmbClient.TabIndex = 0
        '
        'txtAY
        '
        Me.txtAY.Location = New System.Drawing.Point(198, 12)
        Me.txtAY.Name = "txtAY"
        Me.txtAY.Size = New System.Drawing.Size(80, 20)
        Me.txtAY.TabIndex = 1
        '
        'txtNetProfit
        '
        Me.txtNetProfit.Location = New System.Drawing.Point(12, 42)
        Me.txtNetProfit.Name = "txtNetProfit"
        Me.txtNetProfit.Size = New System.Drawing.Size(120, 20)
        Me.txtNetProfit.TabIndex = 2
        '
        'btnSave
        '
        Me.btnSave.Location = New System.Drawing.Point(12, 68)
        Me.btnSave.Name = "btnSave"
        Me.btnSave.Size = New System.Drawing.Size(120, 23)
        Me.btnSave.TabIndex = 3
        Me.btnSave.Text = "Save P&L"
        Me.btnSave.UseVisualStyleBackColor = True
        '
        'PLAccountForm
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(290, 103)
        Me.Controls.Add(Me.btnSave)
        Me.Controls.Add(Me.txtNetProfit)
        Me.Controls.Add(Me.txtAY)
        Me.Controls.Add(Me.cmbClient)
        Me.Name = "PLAccountForm"
        Me.Text = "P&L Account"
        Me.ResumeLayout(False)
        Me.PerformLayout()
    End Sub
End Class
