Attribute VB_Name = "ProofPages"
Option Explicit

' =====================================================================
'  Sign Store - Design Proof import for CorelDRAW (X7 and newer)
'  STAGING version (pairs with the staging Sign Proof Generator)
'
'  ImportDesignProof   Unzip the "... - Design Proof.zip" export, run this
'                      macro and pick the unzipped folder. It makes ONE
'                      new CorelDRAW file with one 11 x 8.5 in page per
'                      SVG in the package (cover page if exported, every
'                      proof page, Proof Summary last), in order p01,
'                      p02 ... Each page is named from package_info.txt.
'                      Then it saves the file as
'                          Ticket# - Customer.cdr
'                      in the job's File Location folder (if it exists on
'                      this computer), otherwise next to the SVG files.
'                      You can edit the name / folder before it saves.
'
'  ImportProductionProofs  Same for the "... - Production.zip" export:
'                      imports the SVG folder of the Production package (QA, proofs +
'                      snapshot, department sheets) into "... - PRODUCTION.cdr".
'
'  How to install: Tools > Scripts > Script Manager (or Alt+F11 for the
'  VBA editor) > GlobalMacros > right-click > Import... > ProofPages.bas.
'  Run it from Tools > Scripts > Run Script (or the Script Manager).
' =====================================================================

Private Const TITLE As String = "Design Proof"
Private Const PAGE_W As Double = 11
Private Const PAGE_H As Double = 8.5


Public Sub ImportDesignProof()
    Dim folder As String
    folder = PickFolder("Select the unzipped Design Proof folder (the one with the p01, p02 ... SVG files), then click OK")
    If folder = "" Then Exit Sub
    If Dir(folder & "*.svg") = "" And Dir(folder & "SVG\*.svg") <> "" Then folder = folder & "SVG\"   ' older packages
    BuildDocument folder, folder, ""
End Sub

Public Sub ImportProductionProofs()
    Dim root As String, folder As String
    root = PickFolder("Select the unzipped Production package folder, then click OK")
    If root = "" Then Exit Sub
    folder = root & "SVG\"
    If Dir(folder & "*.svg") = "" Then folder = root & "Production proofs\SVG\"   ' older packages
    If Dir(folder & "*.svg") = "" Then folder = root            ' picked the SVG folder itself
    BuildDocument folder, root, " - PRODUCTION"
End Sub

' ---------------------------------------------------------------------
Private Sub BuildDocument(ByVal folder As String, ByVal root As String, ByVal suffix As String)
    Dim files() As String, n As Long, i As Long, failed As String
    Dim doc As Document, pg As Page, sr As ShapeRange, info As Object
    Dim k As Double, cx As Double, cy As Double

    n = ListFiles(folder, files)
    If n = 0 Then
        MsgBox "No SVG files found in:" & vbCr & folder & vbCr & vbCr & _
               "Unzip the export first (right-click the zip > Extract All), then pick the unzipped folder.", vbExclamation, TITLE
        Exit Sub
    End If
    Set info = ReadInfo(root & "package_info.txt")
    If info("Ticket") = "" And info("Customer") = "" Then Set info = ReadInfo(ParentFolder(folder) & "package_info.txt")

    ' one new document, letter landscape, one page per SVG
    Set doc = CreateDocument
    doc.Unit = cdrInch
    doc.Pages(1).SetSize PAGE_W, PAGE_H
    If n > 1 Then doc.AddPages n - 1

    doc.BeginCommandGroup "Import " & TITLE
    On Error GoTo ImportError
    For i = 1 To n
        Set pg = doc.Pages(i)
        pg.Activate
        ActiveLayer.Import files(i)
        Set sr = ActiveSelectionRange
        If sr.Count = 0 Then
            failed = failed & vbCr & FileName(files(i))
        Else
            ' page follows the sheet (proof pages landscape, QA pages portrait), sheet fills the page
            If sr.SizeWidth >= sr.SizeHeight Then pg.SetSize PAGE_W, PAGE_H Else pg.SetSize PAGE_H, PAGE_W
            k = pg.SizeWidth / sr.SizeWidth
            If pg.SizeHeight / sr.SizeHeight < k Then k = pg.SizeHeight / sr.SizeHeight
            sr.SetSize sr.SizeWidth * k, sr.SizeHeight * k
            PageCenter pg, cx, cy
            sr.SetPositionEx cdrCenter, cx, cy
            SetPageName pg, PageName(files(i), i, info)
        End If
    Next i
    doc.EndCommandGroup
    doc.Pages(1).Activate
    ActiveWindow.Refresh

    If failed <> "" Then MsgBox "Could not import:" & failed, vbExclamation, TITLE
    NameAndSave doc, root, n, info, suffix
    Exit Sub

ImportError:
    doc.EndCommandGroup
    ActiveWindow.Refresh
    MsgBox "Import stopped on " & FileName(files(i)) & ":" & vbCr & Err.Description, vbExclamation, TITLE
End Sub

' ---------------------------------------------------------------------
'  file name:  Ticket# - Customer.cdr   (from package_info.txt)
' ---------------------------------------------------------------------
Private Sub NameAndSave(doc As Document, ByVal root As String, ByVal nPages As Long, info As Object, ByVal suffix As String)
    Dim ticket As String, customer As String, folder As String, baseName As String, fullPath As String, answer As String

    ticket = info("Ticket"): customer = info("Customer")
    If ticket = "" Then ticket = InputBox("Ticket # for the file name:", TITLE)
    If customer = "" Then customer = InputBox("Customer name for the file name:", TITLE)
    baseName = JoinName(Array(ticket, customer))
    If baseName = "" Then baseName = "Design Proof"
    baseName = baseName & suffix

    ' the job folder from the proof (File Location) if it exists on this computer, else the unzipped folder
    folder = FolderOf(info("FileLocation"))
    If folder = "" Then folder = root

    fullPath = folder & baseName & ".cdr"
    answer = InputBox(nPages & " page(s) imported." & vbCr & vbCr & _
                      "Save the CorelDRAW file as (edit the name or folder if needed;" & vbCr & _
                      "Cancel = don't save now):", TITLE, fullPath)
    If answer = "" Then Exit Sub                 ' Cancel: save later with File > Save As
    If LCase(Right(answer, 4)) <> ".cdr" Then answer = answer & ".cdr"
    If Dir(answer) <> "" Then
        If MsgBox("This file already exists:" & vbCr & answer & vbCr & vbCr & "Replace it?", _
                  vbYesNo + vbExclamation, TITLE) <> vbYes Then Exit Sub
    End If
    On Error GoTo SaveError
    doc.SaveAs answer
    MsgBox "Saved " & nPages & " page(s):" & vbCr & answer, vbInformation, TITLE
    Exit Sub
SaveError:
    MsgBox "Could not save to:" & vbCr & answer & vbCr & vbCr & Err.Description & vbCr & _
           "Use File > Save As instead.", vbExclamation, TITLE
End Sub

' "47601", "Center Parc" -> "47601 - Center Parc"
Private Function JoinName(parts As Variant) As String
    Dim i As Long, p As String, out As String
    For i = LBound(parts) To UBound(parts)
        p = SafeName(CStr(parts(i)))
        If p <> "" Then
            If out <> "" Then out = out & " - "
            out = out & p
        End If
    Next i
    If Len(out) > 150 Then out = Trim(Left(out, 150))
    JoinName = out
End Function

' remove characters Windows does not allow in file names:  \ / : * ? " < > |
Private Function SafeName(ByVal s As String) As String
    Dim bad As Variant, b As Variant
    bad = Array("\", "/", ":", "*", "?", Chr(34), "<", ">", "|", vbTab)
    For Each b In bad
        s = Replace(s, b, " ")
    Next b
    Do While InStr(s, "  ") > 0
        s = Replace(s, "  ", " ")
    Loop
    Do While Right(s, 1) = "." Or Right(s, 1) = " "
        s = Left(s, Len(s) - 1)
        If s = "" Then Exit Do
    Loop
    SafeName = Trim(s)
End Function

' folder part of the proof's File Location, only if it exists on this computer
Private Function FolderOf(ByVal p As String) As String
    Dim f As String
    p = Trim(Replace(p, "/", "\"))
    If p = "" Then Exit Function
    If LCase(Right(p, 4)) = ".cdr" Then
        f = Left(p, InStrRev(p, "\"))
    Else
        f = p
        If Right(f, 1) <> "\" Then f = f & "\"
    End If
    On Error Resume Next
    If f <> "" Then If Dir(f, vbDirectory) <> "" Then FolderOf = f
    On Error GoTo 0
End Function

' package_info.txt (UTF-8, key=value per line) -> dictionary; missing keys read as ""
Private Function ReadInfo(ByVal path As String) As Object
    Dim d As Object, txt As String, lines As Variant, i As Long, p As Long, st As Object, fnum As Integer, k As Variant
    Set d = CreateObject("Scripting.Dictionary")
    d.CompareMode = 1
    For Each k In Array("Ticket", "Customer", "SubCustomer", "Project", "FileLocation", "FileBase")
        d(k) = ""
    Next k
    If Dir(path) = "" Then Set ReadInfo = d: Exit Function
    On Error Resume Next
    Set st = CreateObject("ADODB.Stream")
    If Not st Is Nothing Then
        st.Type = 2: st.Charset = "utf-8": st.Open: st.LoadFromFile path: txt = st.ReadText: st.Close
    End If
    If txt = "" Then
        fnum = FreeFile: Open path For Input As #fnum: txt = Input$(LOF(fnum), fnum): Close #fnum
    End If
    On Error GoTo 0
    If Left(txt, 1) = ChrW(&HFEFF) Then txt = Mid(txt, 2)
    lines = Split(Replace(txt, vbCr, ""), vbLf)
    For i = LBound(lines) To UBound(lines)
        p = InStr(lines(i), "=")
        If p > 1 Then d(Trim(Left(lines(i), p - 1))) = Trim(Mid(lines(i), p + 1))
    Next i
    Set ReadInfo = d
End Function

' ---------------------------------------------------------------------
'  helpers
' ---------------------------------------------------------------------
Private Function PickFolder(ByVal prompt As String) As String
    ' Windows "Browse for Folder" window; the box at the bottom also accepts a pasted path
    Dim sh As Object, fld As Object, f As String
    On Error Resume Next
    Set sh = CreateObject("Shell.Application")
    Set fld = sh.BrowseForFolder(0, prompt, &H10 Or &H40 Or &H200, 0)
    If Not fld Is Nothing Then f = fld.Self.Path
    If sh Is Nothing Then f = InputBox("Paste the path of the unzipped folder:", TITLE)
    On Error GoTo 0
    If f <> "" And Right(f, 1) <> "\" Then f = f & "\"
    PickFolder = f
End Function

Private Function ParentFolder(ByVal f As String) As String
    Dim p As Long
    If Right(f, 1) = "\" Then f = Left(f, Len(f) - 1)
    p = InStrRev(f, "\")
    If p > 0 Then ParentFolder = Left(f, p) Else ParentFolder = f & "\"
End Function

' the SVG files in a folder, full paths, sorted by name (p01, p02 ... / prod01, prod02 ...)
Private Function ListFiles(ByVal folder As String, files() As String) As Long
    Dim n As Long, f As String, i As Long, j As Long, t As String
    f = Dir(folder & "*.svg")
    Do While f <> ""
        n = n + 1
        ReDim Preserve files(1 To n)
        files(n) = folder & f
        f = Dir()
    Loop
    For i = 1 To n - 1
        For j = i + 1 To n
            If LCase(files(j)) < LCase(files(i)) Then t = files(i): files(i) = files(j): files(j) = t
        Next j
    Next i
    ListFiles = n
End Function

' page names are set through a late-bound object so this compiles in every CorelDRAW version
Private Sub SetPageName(pg As Page, ByVal nm As String)
    Dim o As Object
    Set o = pg
    On Error Resume Next
    o.Name = nm
    On Error GoTo 0
End Sub

Private Sub PageCenter(pg As Page, cx As Double, cy As Double)
    Dim o As Object
    Set o = pg                                     ' late-bound: compiles in every version
    cx = pg.SizeWidth / 2: cy = pg.SizeHeight / 2
    On Error Resume Next
    cx = (o.LeftX + o.RightX) / 2
    cy = (o.TopY + o.BottomY) / 2
    On Error GoTo 0
End Sub

Private Function FileName(ByVal path As String) As String
    FileName = Mid(path, InStrRev(path, "\") + 1)
End Function

' Page name for CorelDRAW from package_info.txt (Page01=COVER, Page02=MONUMENT SIGNS 1/3 ... last=PROOF SUMMARY);
' production files: "47601 - prod03.svg" -> PRODUCTION 3, "... - color chart" -> COLOR CHART
Private Function PageName(ByVal path As String, ByVal i As Long, info As Object) As String
    Dim s As String, key As String
    s = FileName(path)
    s = Left(s, InStrRev(s, ".") - 1)
    If LCase(s) Like "* - p##" Then
        key = "Page" & Right(s, 2)
        If info.Exists(key) Then
            If info(key) <> "" Then PageName = info(key): Exit Function
        End If
        PageName = "PAGE " & CLng(Right(s, 2)): Exit Function
    End If
    If LCase(s) Like "*color chart" Then PageName = "COLOR CHART": Exit Function
    If LCase(s) Like "* - qa##" Then PageName = "QA SHEET " & CLng(Right(s, 2)): Exit Function
    If LCase(s) Like "* - prod##" Then PageName = "PRODUCTION " & CLng(Right(s, 2)): Exit Function
    If LCase(s) Like "* - prod## - snapshot" Then PageName = "PRODUCTION SNAPSHOT": Exit Function
    If LCase(s) Like "* - prod## - dept *" Then PageName = UCase(Mid(s, InStrRev(LCase(s), " - dept ") + 8)) & " DEPARTMENT": Exit Function
    PageName = "PAGE " & i
End Function
