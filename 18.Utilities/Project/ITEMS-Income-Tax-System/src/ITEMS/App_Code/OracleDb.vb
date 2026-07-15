' =============================================================================
' ITEMS · OracleDb.vb — thin data-access helper over ODP.NET (managed)
' Centralises connection handling and parameterised commands (prevents SQL
' injection). Every module's repository builds on these primitives.
' =============================================================================
Imports System.Configuration
Imports System.Data
Imports Oracle.ManagedDataAccess.Client

Namespace Data

    Public NotInheritable Class OracleDb

        Private Sub New()
        End Sub

        Private Shared ReadOnly Property ConnString As String
            Get
                Return ConfigurationManager.ConnectionStrings("ItemsDb").ConnectionString
            End Get
        End Property

        Public Shared Function OpenConnection() As OracleConnection
            Dim cn As New OracleConnection(ConnString)
            cn.Open()
            Return cn
        End Function

        ''' <summary>Runs a query and returns a filled DataTable.</summary>
        Public Shared Function Query(sql As String, ParamArray ps As OracleParameter()) As DataTable
            Using cn = OpenConnection()
                Using cmd As New OracleCommand(sql, cn)
                    cmd.BindByName = True
                    If ps IsNot Nothing Then cmd.Parameters.AddRange(ps)
                    Using da As New OracleDataAdapter(cmd)
                        Dim dt As New DataTable()
                        da.Fill(dt)
                        Return dt
                    End Using
                End Using
            End Using
        End Function

        ''' <summary>Runs a query and returns the first row, or Nothing.</summary>
        Public Shared Function QueryRow(sql As String, ParamArray ps As OracleParameter()) As DataRow
            Dim dt = Query(sql, ps)
            Return If(dt.Rows.Count > 0, dt.Rows(0), Nothing)
        End Function

        ''' <summary>Executes INSERT / UPDATE / DELETE and returns rows affected.</summary>
        Public Shared Function Execute(sql As String, ParamArray ps As OracleParameter()) As Integer
            Using cn = OpenConnection()
                Using cmd As New OracleCommand(sql, cn)
                    cmd.BindByName = True
                    If ps IsNot Nothing Then cmd.Parameters.AddRange(ps)
                    Return cmd.ExecuteNonQuery()
                End Using
            End Using
        End Function

        Public Shared Function Scalar(sql As String, ParamArray ps As OracleParameter()) As Object
            Using cn = OpenConnection()
                Using cmd As New OracleCommand(sql, cn)
                    cmd.BindByName = True
                    If ps IsNot Nothing Then cmd.Parameters.AddRange(ps)
                    Return cmd.ExecuteScalar()
                End Using
            End Using
        End Function

        ' -- Parameter factories -------------------------------------------------
        Public Shared Function P(name As String, value As Object) As OracleParameter
            Return New OracleParameter(name, If(value, DBNull.Value))
        End Function

        Public Shared Function PStr(name As String, value As String) As OracleParameter
            Return New OracleParameter(name, OracleDbType.Varchar2) With {.Value = If(value, CObj(DBNull.Value))}
        End Function

        Public Shared Function PNum(name As String, value As Decimal) As OracleParameter
            Return New OracleParameter(name, OracleDbType.Decimal) With {.Value = value}
        End Function

        Public Shared Function PDate(name As String, value As Date?) As OracleParameter
            Return New OracleParameter(name, OracleDbType.Date) With {.Value = If(value.HasValue, CObj(value.Value), DBNull.Value)}
        End Function

    End Class

End Namespace
