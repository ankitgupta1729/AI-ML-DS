Partial Class TradingAccountForm
    Friend WithEvents cmbClient As System.Windows.Forms.ComboBox
    Friend WithEvents txtAY As System.Windows.Forms.TextBox
    Friend WithEvents txtOB As System.Windows.Forms.TextBox
    Friend WithEvents txtPurchases As System.Windows.Forms.TextBox
    Friend WithEvents txtSales As System.Windows.Forms.TextBox
    Friend WithEvents btnSave As System.Windows.Forms.Button

    Private Sub InitializeComponent()
        Me.cmbClient = New System.Windows.Forms.ComboBox()
        Me.txtAY = New System.Windows.Forms.TextBox()
        Me.txtOB = New System.Windows.Forms.TextBox()
        Me.txtPurchases = New System.Windows.Forms.TextBox()
        Me.txtSales = New System.Windows.Forms.TextBox()
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
        'txtOB
        '
        Me.txtOB.Location = New System.Drawing.Point(12, 42)
        Me.txtOB.Name = "txtOB"
        Me.txtOB.Size = New System.Drawing.Size(120, 20)
        Me.txtOB.TabIndex = 2
        '
        'txtPurchases
        '
        Me.txtPurchases.Location = New System.Drawing.Point(138, 42)
        Me.txtPurchases.Name = "txtPurchases"
        Me.txtPurchases.Size = New System.Drawing.Size(120, 20)
        Me.txtPurchases.TabIndex = 3
        '
        'txtSales
        '
        Me.txtSales.Location = New System.Drawing.Point(12, 68)
        Me.txtSales.Name = "txtSales"
        Me.txtSales.Size = New System.Drawing.Size(120, 20)
        Me.txtSales.TabIndex = 4
        '
        'btnSave
        '
        Me.btnSave.Location = New System.Drawing.Point(12, 94)
        Me.btnSave.Name = "btnSave"
        Me.btnSave.Size = New System.Drawing.Size(120, 23)
        Me.btnSave.TabIndex = 5
        Me.btnSave.Text = "Save Trading"
        Me.btnSave.UseVisualStyleBackColor = True
        '
        'TradingAccountForm
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(284, 129)
        Me.Controls.Add(Me.btnSave)
        Me.Controls.Add(Me.txtSales)
        Me.Controls.Add(Me.txtPurchases)
        Me.Controls.Add(Me.txtOB)
        Me.Controls.Add(Me.txtAY)
        Me.Controls.Add(Me.cmbClient)
        Me.Name = "TradingAccountForm"
        Me.Text = "Trading Account"
        Me.ResumeLayout(False)
        Me.PerformLayout()
    End Sub
End Class
