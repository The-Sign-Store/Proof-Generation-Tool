Attribute VB_Name = "ProofPages"
Option Explicit

' =====================================================================
'  Sign Store - proof page tools for CorelDRAW (X7 and newer)
'
'  AddProofPages     Asks how many pages the proof needs and adds the
'                    missing ones at 11 x 8.5 landscape. Existing pages
'                    are never resized or deleted.
'
'  BuildFromPackage  Pick the UNZIPPED Proof Generator package folder.
'                    Makes a new document with one 11 x 8.5 page per SVG,
'                    in package order (p01, p02 ...), imports each sheet
'                    onto its page and names the page from the file.
' =====================================================================

Private Const PAGE_W As Double = 11
Private Const PAGE_H As Double = 8.5

Public Sub AddProofPages()
    Dim doc As Document, answer As String, total As Long, need As Long
    Dim firstNew As Long, i As Long

    If Documents.Count = 0 Then
        Set doc = CreateDocument
    Else
        Set doc = ActiveDocument
    End If

    answer = InputBox("How many pages does this proof need in total?" & vbCr & _
                      "This document has " & doc.Pages.Count & " page(s) now.", _
                      "Proof Pages", CStr(doc.Pages.Count))
    If answer = "" Then Exit Sub
    If Not IsNumeric(answer) Then
        MsgBox "Please enter a number.", vbExclamation, "Proof Pages"
        Exit Sub
    End If

    total = CLng(answer)
    need = total - doc.Pages.Count
    If need < 0 Then
        MsgBox "This document already has " & doc.Pages.Count & " pages." & vbCr & _
               "Delete extra pages by hand so no artwork is lost.", vbExclamation, "Proof Pages"
        Exit Sub
    End If

    doc.Unit = cdrInch
    If need > 0 Then
        firstNew = doc.Pages.Count + 1
        doc.BeginCommandGroup "Add proof pages"      ' one Ctrl+Z undoes it all
        doc.AddPages need
        For i = firstNew To doc.Pages.Count
            doc.Pages(i).SetSize PAGE_W, PAGE_H      ' new pages only
        Next i
        doc.EndCommandGroup
    End If

    doc.Pages(1).Activate
    MsgBox "This document now has " & doc.Pages.Count & " pages.", vbInformation, "Proof Pages"
End Sub

Public Sub BuildFromPackage()
    Dim folder As String, f As String, files() As String, n As Long
    Dim i As Long, j As Long, t As String
    Dim doc As Document, pg As Page, sr As ShapeRange

    ' 1) pick the folder (unzip the package first)
    On Error Resume Next
    folder = CorelScriptTools.GetFolder("", "Select the UNZIPPED proof package folder")
    On Error GoTo 0
    If folder = "" Then folder = InputBox("Paste the path of the unzipped proof package folder:", "Proof Package")
    If folder = "" Then Exit Sub
    If Right(folder, 1) <> "\" Then folder = folder & "\"

    ' 2) list the SVG sheets
    f = Dir(folder & "*.svg")
    Do While f <> ""
        n = n + 1
        ReDim Preserve files(1 To n)
        files(n) = f
        f = Dir()
    Loop
    If n = 0 Then
        MsgBox "No .svg files found in:" & vbCr & folder & vbCr & vbCr & _
               "Unzip the proof package first, then pick that folder.", vbExclamation, "Proof Package"
        Exit Sub
    End If

    ' 3) sort by file name so p01, p02 ... keep the package order
    For i = 1 To n - 1
        For j = i + 1 To n
            If LCase(files(j)) < LCase(files(i)) Then
                t = files(i): files(i) = files(j): files(j) = t
            End If
        Next j
    Next i

    ' 4) one page per sheet
    Set doc = CreateDocument
    doc.Unit = cdrInch
    doc.ReferencePoint = cdrTopLeft
    If n > 1 Then doc.AddPages n - 1

    For i = 1 To n
        Set pg = doc.Pages(i)
        pg.SetSize PAGE_W, PAGE_H
        pg.Name = PageName(files(i))
        pg.Activate
        ActiveLayer.Import folder & files(i)
        Set sr = ActiveSelectionRange
        If sr.Count > 0 Then
            sr.SetSize PAGE_W, PAGE_H                ' the sheet is exactly one page
            sr.SetPosition pg.LeftX, pg.TopY
        End If
    Next i

    doc.Pages(1).Activate
    MsgBox n & " proof pages built from:" & vbCr & folder & vbCr & vbCr & _
           "Save the file with the job name (Ticket#_Customer_Product_R0.cdr).", vbInformation, "Proof Package"
End Sub

' p02_pole_sign_specs_2.svg  ->  POLE SIGN SPECS 2
Private Function PageName(ByVal fileName As String) As String
    Dim s As String
    s = Left(fileName, Len(fileName) - 4)
    If s Like "p##_*" Then s = Mid(s, 5)
    PageName = UCase(Replace(s, "_", " "))
End Function
