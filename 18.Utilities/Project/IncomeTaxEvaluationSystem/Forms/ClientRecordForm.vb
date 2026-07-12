Public Class ClientRecordForm
    Private Sub btnNew_Click(sender As Object, e As EventArgs) Handles btnNew.Click
        clearForm()
    End Sub

    Private Sub btnSave_Click(sender As Object, e As EventArgs) Handles btnSave.Click
        Dim code = txtCode.Text.Trim()
        Dim name = txtName.Text.Trim()
        Dim pan = txtPAN.Text.Trim().ToUpper()
        If String.IsNullOrEmpty(code) OrElse String.IsNullOrEmpty(name) OrElse String.IsNullOrEmpty(pan) Then
            MessageBox.Show("Client Code, Name and PAN are required", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        If Not Modules.Validation.IsValidPAN(pan) Then
            MessageBox.Show("Invalid PAN format (e.g., ABCDE1234F)", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If
        Dim record As New Models.ClientRecord()
        record.ClientCode = code
        record.FullName = name
        record.PAN = pan
        record.Gender = cmbGender.Text
        record.City = txtCity.Text.Trim()
        record.Mobile = txtMobile.Text.Trim()
        record.AssessmentYear = txtAY.Text.Trim()
        record.CreatedBy = MainForm.UserId
        record.UpdatedBy = MainForm.UserId
        Data.OracleDataAccess.InsertUpdateClient(record)
        MessageBox.Show("Saved successfully", "Info", MessageBoxButtons.OK, MessageBoxIcon.Information)
        loadGrid()
    End Sub

    Private Sub btnDelete_Click(sender As Object, e As EventArgs) Handles btnDelete.Click
        If String.IsNullOrEmpty(txtCode.Text) Then Return
        If MessageBox.Show("Delete record?", "Confirm", MessageBoxButtons.YesNo) = DialogResult.Yes Then
            Data.OracleDataAccess.DeleteClient(txtCode.Text.Trim())
            clearForm()
            loadGrid()
        End If
    End Sub

    Private Sub txtSearch_TextChanged(sender As Object, e As EventArgs) Handles txtSearch.TextChanged
        loadGrid()
    End Sub

    Private Sub loadGrid()
        Dim dt = Data.OracleDataAccess.GetAllClients(txtSearch.Text.Trim())
        dgv.DataSource = dt
    End Sub

    Private Sub clearForm()
        txtCode.Clear() : txtName.Clear() : txtPAN.Clear() : txtCity.Clear()
        txtMobile.Clear() : txtAY.Clear() : cmbGender.SelectedIndex = -1
    End Sub

    Private Sub ClientRecordForm_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        loadGrid()
    End Sub
End Class