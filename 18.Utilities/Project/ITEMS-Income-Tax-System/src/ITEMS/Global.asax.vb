' =============================================================================
' ITEMS · Global.asax.vb — application lifecycle hooks
' =============================================================================
Imports System.Web

Namespace ITEMS

    Public Class Global_asax
        Inherits HttpApplication

        Sub Application_Start(sender As Object, e As EventArgs)
            ' Reserved for start-up wiring (routing, logging, etc.).
        End Sub

        Sub Application_Error(sender As Object, e As EventArgs)
            ' Central place to log unhandled exceptions.
            Dim ex = Server.GetLastError()
            System.Diagnostics.Trace.TraceError("ITEMS unhandled: " & If(ex IsNot Nothing, ex.ToString(), "n/a"))
        End Sub

    End Class

End Namespace
