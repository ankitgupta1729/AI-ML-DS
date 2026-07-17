' =============================================================================
' Income Tax Evaluation System · ClientRepository.vb — CRUD for the Client Information module
' =============================================================================
Imports System.Collections.Generic
Imports System.Data
Imports ITEMS.Data
Imports ITEMS.Models

Namespace Repositories

    Public NotInheritable Class ClientRepository

        Private Sub New()
        End Sub

        Private Shared Function Map(r As DataRow) As Client
            Return New Client With {
                .Pan = Convert.ToString(r("PAN")),
                .Name = Convert.ToString(r("CLIENT_NAME")),
                .FathersName = Convert.ToString(r("FATHERS_NAME")),
                .Dob = If(IsDBNull(r("DOB")), CType(Nothing, Date?), Convert.ToDateTime(r("DOB"))),
                .Pincode = Convert.ToString(r("PINCODE")),
                .Address = Convert.ToString(r("ADDRESS")),
                .Telephone = Convert.ToString(r("TELEPHONE")),
                .Sex = ToInt(r("SEX")),
                .Category = ToInt(r("INDV_HUF_FIRM_AOP_LA")),
                .Residence = ToInt(r("RESIDENT_NR_NOR")),
                .WardCircleRange = Convert.ToString(r("WARD_CIRCLE_SPECIAL_RANGE"))
            }
        End Function

        Private Shared Function ToInt(o As Object) As Integer
            Return If(IsDBNull(o), 0, Convert.ToInt32(o))
        End Function

        Public Shared Function GetAll(Optional search As String = Nothing) As List(Of Client)
            Dim sql = "SELECT * FROM CLIENT_RECORD"
            Dim dt As DataTable
            If String.IsNullOrWhiteSpace(search) Then
                sql &= " ORDER BY CLIENT_NAME"
                dt = OracleDb.Query(sql)
            Else
                sql &= " WHERE UPPER(CLIENT_NAME) LIKE :q OR UPPER(PAN) LIKE :q OR UPPER(ADDRESS) LIKE :q ORDER BY CLIENT_NAME"
                dt = OracleDb.Query(sql, OracleDb.PStr("q", "%" & search.Trim().ToUpperInvariant() & "%"))
            End If
            Dim list As New List(Of Client)()
            For Each r As DataRow In dt.Rows
                list.Add(Map(r))
            Next
            Return list
        End Function

        Public Shared Function GetFirms() As List(Of Client)
            Return GetAll().FindAll(Function(c) c.IsFirm)
        End Function

        Public Shared Function [Get](pan As String) As Client
            Dim r = OracleDb.QueryRow("SELECT * FROM CLIENT_RECORD WHERE PAN = :p", OracleDb.PStr("p", pan))
            Return If(r Is Nothing, Nothing, Map(r))
        End Function

        Public Shared Function Exists(pan As String) As Boolean
            Return Convert.ToInt32(OracleDb.Scalar("SELECT COUNT(*) FROM CLIENT_RECORD WHERE PAN = :p", OracleDb.PStr("p", pan))) > 0
        End Function

        Public Shared Sub Insert(c As Client)
            OracleDb.Execute(
                "INSERT INTO CLIENT_RECORD (PAN,CLIENT_NAME,FATHERS_NAME,DOB,PINCODE,ADDRESS,TELEPHONE,SEX,INDV_HUF_FIRM_AOP_LA,RESIDENT_NR_NOR,WARD_CIRCLE_SPECIAL_RANGE) " &
                "VALUES (:pan,:nm,:fn,:dob,:pin,:addr,:tel,:sex,:cat,:res,:ward)",
                OracleDb.PStr("pan", c.Pan.ToUpperInvariant()), OracleDb.PStr("nm", c.Name), OracleDb.PStr("fn", c.FathersName),
                OracleDb.PDate("dob", c.Dob), OracleDb.PStr("pin", c.Pincode), OracleDb.PStr("addr", c.Address),
                OracleDb.PStr("tel", c.Telephone), OracleDb.PNum("sex", c.Sex), OracleDb.PNum("cat", c.Category),
                OracleDb.PNum("res", c.Residence), OracleDb.PStr("ward", c.WardCircleRange))
        End Sub

        Public Shared Sub Update(c As Client)
            OracleDb.Execute(
                "UPDATE CLIENT_RECORD SET CLIENT_NAME=:nm,FATHERS_NAME=:fn,DOB=:dob,PINCODE=:pin,ADDRESS=:addr," &
                "TELEPHONE=:tel,SEX=:sex,INDV_HUF_FIRM_AOP_LA=:cat,RESIDENT_NR_NOR=:res,WARD_CIRCLE_SPECIAL_RANGE=:ward WHERE PAN=:pan",
                OracleDb.PStr("nm", c.Name), OracleDb.PStr("fn", c.FathersName), OracleDb.PDate("dob", c.Dob),
                OracleDb.PStr("pin", c.Pincode), OracleDb.PStr("addr", c.Address), OracleDb.PStr("tel", c.Telephone),
                OracleDb.PNum("sex", c.Sex), OracleDb.PNum("cat", c.Category), OracleDb.PNum("res", c.Residence),
                OracleDb.PStr("ward", c.WardCircleRange), OracleDb.PStr("pan", c.Pan))
        End Sub

        ''' <summary>Delete cascades to returns / accounts via FK ON DELETE CASCADE.</summary>
        Public Shared Sub Delete(pan As String)
            OracleDb.Execute("DELETE FROM CLIENT_RECORD WHERE PAN = :p", OracleDb.PStr("p", pan))
        End Sub

    End Class

End Namespace
