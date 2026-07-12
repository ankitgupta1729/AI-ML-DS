Namespace Modules

    Public Module Validation

        Public Function IsValidPAN(pan As String) As Boolean
            Return System.Text.RegularExpressions.Regex.IsMatch(pan.ToUpper(), "^[A-Z]{5}[0-9]{4}[A-Z]$")
        End Function

        Public Function IsValidPincode(pin As String) As Boolean
            Return System.Text.RegularExpressions.Regex.IsMatch(pin, "^[0-9]{6}$")
        End Function

        Public Function IsValidTelephone(tel As String) As Boolean
            Return String.IsNullOrEmpty(tel) OrElse System.Text.RegularExpressions.Regex.IsMatch(tel, "^\+?[0-9\-]{10,15}$")
        End Function

        Public Function IsValidMobile(mobile As String) As Boolean
            Return System.Text.RegularExpressions.Regex.IsMatch(mobile, "^[0-9]{10}$")
        End Function

        Public Function IsValidDate(dateStr As String) As Boolean
            Dim d As Date
            Return Date.TryParse(dateStr, d)
        End Function

        Public Function IsValidEmail(email As String) As Boolean
            Return String.IsNullOrEmpty(email) OrElse System.Text.RegularExpressions.Regex.IsMatch(email, "^[^@\s]+@[^@\s]+\.[^@\s]+$")
        End Function

        Public Function IsValidAadhar(aadhar As String) As Boolean
            Return String.IsNullOrEmpty(aadhar) OrElse System.Text.RegularExpressions.Regex.IsMatch(aadhar, "^[0-9]{12}$")
        End Function

        Public Function IsAlphaNumeric(value As String) As Boolean
            Return System.Text.RegularExpressions.Regex.IsMatch(value, "^[a-zA-Z0-9\s]+$")
        End Function

        Public Function IsValidAssessmentYear(year As String) As Boolean
            Return System.Text.RegularExpressions.Regex.IsMatch(year, "^[0-9]{4}-[0-9]{2}$")
        End Function

        Public Function ValidateClientRecord(record As Models.ClientRecord) As List(Of String)
            Dim errors As New List(Of String)()
            If String.IsNullOrEmpty(record.ClientCode) Then errors.Add("Client Code is required")
            If String.IsNullOrEmpty(record.FullName) Then errors.Add("Full Name is required")
            If Not IsValidPAN(record.PAN) Then errors.Add("Invalid PAN format (e.g., ABCDE1234F)")
            If record.DateOfBirth <> Date.MinValue AndAlso record.DateOfBirth > Date.Today Then errors.Add("Date of Birth cannot be future")
            If String.IsNullOrEmpty(record.Gender) OrElse Not {"Male", "Female", "Other"}.Contains(record.Gender) Then errors.Add("Gender is required (Male/Female/Other)")
            If Not String.IsNullOrEmpty(record.Pincode) AndAlso Not IsValidPincode(record.Pincode) Then errors.Add("Invalid Pincode (6 digits)")
            If Not String.IsNullOrEmpty(record.Telephone) AndAlso Not IsValidTelephone(record.Telephone) Then errors.Add("Invalid Telephone number")
            If Not String.IsNullOrEmpty(record.Mobile) AndAlso Not IsValidMobile(record.Mobile) Then errors.Add("Invalid Mobile number (10 digits)")
            If Not String.IsNullOrEmpty(record.Email) AndAlso Not IsValidEmail(record.Email) Then errors.Add("Invalid Email format")
            If Not String.IsNullOrEmpty(record.AadharNumber) AndAlso Not IsValidAadhar(record.AadharNumber) Then errors.Add("Invalid Aadhar (12 digits)")
            Return errors
        End Function

    End Module

End Namespace
