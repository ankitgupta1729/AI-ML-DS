Partial Class IncomeTaxRecordForm
    Friend WithEvents cmbClient As System.Windows.Forms.ComboBox
    Friend WithEvents txtAY As System.Windows.Forms.TextBox
    Friend WithEvents txtSalary As System.Windows.Forms.TextBox
    Friend WithEvents txtHouse As System.Windows.Forms.TextBox
    Friend WithEvents txtBusiness As System.Windows.Forms.TextBox
    Friend WithEvents txtCapital As System.Windows.Forms.TextBox
    Friend WithEvents txtOther As System.Windows.Forms.TextBox
    Friend WithEvents txt80C As System.Windows.Forms.TextBox
    Friend WithEvents txt80D As System.Windows.Forms.TextBox
    Friend WithEvents txt80G As System.Windows.Forms.TextBox
    Friend WithEvents txtOtherDed As System.Windows.Forms.TextBox
    Friend WithEvents btnSave As System.Windows.Forms.Button

    Private Sub InitializeComponent()
        Me.cmbClient = New System.Windows.Forms.ComboBox()
        Me.txtAY = New System.Windows.Forms.TextBox()
        Me.txtSalary = New System.Windows.Forms.TextBox()
        Me.txtHouse = New System.Windows.Forms.TextBox()
        Me.txtBusiness = New System.Windows.Forms.TextBox()
        Me.txtCapital = New System.Windows.Forms.TextBox()
        Me.txtOther = New System.Windows.Forms.TextBox()
        Me.txt80C = New System.Windows.Forms.TextBox()
        Me.txt80D = New System.Windows.Forms.TextBox()
        Me.txt80G = New System.Windows.Forms.TextBox()
        Me.txtOtherDed = New System.Windows.Forms.TextBox()
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
        'txtSalary
        '
        Me.txtSalary.Location = New System.Drawing.Point(12, 42)
        Me.txtSalary.Name = "txtSalary"
        Me.txtSalary.Size = New System.Drawing.Size(120, 20)
        Me.txtSalary.TabIndex = 2
        '
        'txtHouse
        '
        Me.txtHouse.Location = New System.Drawing.Point(138, 42)
        Me.txtHouse.Name = "txtHouse"
        Me.txtHouse.Size = New System.Drawing.Size(120, 20)
        Me.txtHouse.TabIndex = 3
        '
        'txtBusiness
        '
        Me.txtBusiness.Location = New System.Drawing.Point(264, 42)
        Me.txtBusiness.Name = "txtBusiness"
        Me.txtBusiness.Size = New System.Drawing.Size(120, 20)
        Me.txtBusiness.TabIndex = 4
        '
        'txtCapital
        '
        Me.txtCapital.Location = New System.Drawing.Point(12, 68)
        Me.txtCapital.Name = "txtCapital"
        Me.txtCapital.Size = New System.Drawing.Size(120, 20)
        Me.txtCapital.TabIndex = 5
        '
        'txtOther
        '
        Me.txtOther.Location = New System.Drawing.Point(138, 68)
        Me.txtOther.Name = "txtOther"
        Me.txtOther.Size = New System.Drawing.Size(120, 20)
        Me.txtOther.TabIndex = 6
        '
        'txt80C
        '
        Me.txt80C.Location = New System.Drawing.Point(12, 94)
        Me.txt80C.Name = "txt80C"
        Me.txt80C.Size = New System.Drawing.Size(120, 20)
        Me.txt80C.TabIndex = 7
        '
        'txt80D
        '
        Me.txt80D.Location = New System.Drawing.Point(138, 94)
        Me.txt80D.Name = "txt80D"
        Me.txt80D.Size = New System.Drawing.Size(120, 20)
        Me.txt80D.TabIndex = 8
        '
        'txt80G
        '
        Me.txt80G.Location = New System.Drawing.Point(264, 94)
        Me.txt80G.Name = "txt80G"
        Me.txt80G.Size = New System.Drawing.Size(120, 20)
        Me.txt80G.TabIndex = 9
        '
        'txtOtherDed
        '
        Me.txtOtherDed.Location = New System.Drawing.Point(12, 120)
        Me.txtOtherDed.Name = "txtOtherDed"
        Me.txtOtherDed.Size = New System.Drawing.Size(120, 20)
        Me.txtOtherDed.TabIndex = 10
        '
        'btnSave
        '
        Me.btnSave.Location = New System.Drawing.Point(12, 146)
        Me.btnSave.Name = "btnSave"
        Me.btnSave.Size = New System.Drawing.Size(120, 23)
        Me.btnSave.TabIndex = 11
        Me.btnSave.Text = "Save"
        Me.btnSave.UseVisualStyleBackColor = True
        '
        'IncomeTaxRecordForm
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(400, 181)
        Me.Controls.Add(Me.btnSave)
        Me.Controls.Add(Me.txtOtherDed)
        Me.Controls.Add(Me.txt80G)
        Me.Controls.Add(Me.txt80D)
        Me.Controls.Add(Me.txt80C)
        Me.Controls.Add(Me.txtOther)
        Me.Controls.Add(Me.txtCapital)
        Me.Controls.Add(Me.txtBusiness)
        Me.Controls.Add(Me.txtHouse)
        Me.Controls.Add(Me.txtSalary)
        Me.Controls.Add(Me.txtAY)
        Me.Controls.Add(Me.cmbClient)
        Me.Name = "IncomeTaxRecordForm"
        Me.Text = "Income Tax Record"
        Me.ResumeLayout(False)
        Me.PerformLayout()
    End Sub
End Class
