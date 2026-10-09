Attribute VB_Name = "ProofPages"
Option Explicit

' =====================================================================
'  Sign Store - proof package tools for CorelDRAW (X7 and newer)
'
'  ImportProofPackage  Run it in the document made from your proof
'                      template (File > New from Template). Pick the
'                      unzipped proof package folder or its SVG folder.
'                      One page per file, in package order (p01, p02 ...):
'                      the first empty page is used, pages are added as
'                      needed, each sheet is imported and scaled to FILL
'                      its page, the page turns landscape / portrait to
'                      match the sheet, and the page is named from the
'                      file. Optionally adds the QA checklist pages too.
'                      One Ctrl+Z (Undo) removes the whole import.
'                      Then it saves the file as
'                        Ticket# - Customer - [Sub-Customer -] Project.cdr
'                      using package_info.txt from the package (you can
'                      edit the name / folder before it saves).
'
'  BuildFromPackage    Same import into a brand-new letter-size document.
'
'  AddProofPages       Asks how many pages the proof needs and adds the
'                      missing ones (existing pages are left alone).
' =====================================================================

Private Const TITLE As String = "Proof Package"
Private Const LETTER_SHORT As Double = 8.5
Private Const LETTER_LONG As Double = 11


Public Sub ImportProofPackage()
    If Documents.Count = 0 Then
        MsgBox "Open your proof template first (File > New from Template)," & vbCr & _
               "then run ImportProofPackage again.", vbExclamation, TITLE
        Exit Sub
    End If
    ImportInto ActiveDocument
End Sub

Public Sub BuildFromPackage()
    Dim doc As Document
    Set doc = CreateDocument
    doc.Unit = cdrInch
    doc.Pages(1).SetSize LETTER_LONG, LETTER_SHORT
    ImportInto doc
End Sub

' ---------------------------------------------------------------------
Private Sub ImportInto(doc As Document)
    Dim folder As String, qaFolder As String, root As String, files() As String, n As Long, nProof As Long
    Dim i As Long, idx As Long, startIdx As Long, failed As String
    Dim pg As Page, sr As ShapeRange
    Dim shortSide As Double, longSide As Double, k As Double, cx As Double, cy As Double
    Dim info As Object

    ' 1) folders: proof sheets (SVG) and, if present, the QA checklist
    folder = PickFolder()
    If folder = "" Then Exit Sub
    If Dir(folder & "*.svg") = "" And Dir(folder & "SVG\*.svg") <> "" Then
        root = folder                                           ' picked the package folder
        folder = folder & "SVG\"
    Else
        root = ParentFolder(folder)                             ' picked the SVG folder itself
    End If
    qaFolder = root & "QA_Checklist\SVG\"
    Set info = ReadInfo(root & "package_info.txt")        ' job details + page names from the export

    n = ListFiles(folder, files)
    If n = 0 Then
        MsgBox "No SVG (or PNG / JPG) files found in:" & vbCr & folder & vbCr & vbCr & _
               "Unzip the proof package first, then pick its folder or its SVG folder.", vbExclamation, TITLE
        Exit Sub
    End If
    nProof = n
    If Dir(qaFolder & "*.svg") <> "" Then
        If MsgBox("Also add the QA checklist pages at the end?" & vbCr & vbCr & _
                  "(They are for the QA manager, not the customer.)", vbYesNo + vbQuestion, TITLE) = vbYes Then
            n = AppendFiles(qaFolder, files, n)
        End If
    End If

    ' 2) page size comes from the template's first page (8.5 x 11 in either orientation)
    doc.Unit = cdrInch
    shortSide = doc.Pages(1).SizeWidth: longSide = doc.Pages(1).SizeHeight
    If shortSide > longSide Then k = shortSide: shortSide = longSide: longSide = k
    If shortSide <= 0 Then shortSide = LETTER_SHORT: longSide = LETTER_LONG

    ' 3) start on the first empty page at the end of the document (the template's blank page)
    startIdx = doc.Pages.Count + 1
    Do While startIdx > 1
        If PageHasArt(doc.Pages(startIdx - 1)) Then Exit Do
        startIdx = startIdx - 1
    Loop
    If startIdx > 1 Then
        If MsgBox("This document already has " & (startIdx - 1) & " page(s) with artwork." & vbCr & _
                  "Add the " & n & " proof page(s) after them?", vbOKCancel + vbQuestion, TITLE) <> vbOK Then Exit Sub
    End If

    ' 4) import: one page per file
    doc.BeginCommandGroup "Import proof package"
    On Error GoTo ImportError
    For i = 1 To n
        idx = startIdx + i - 1
        If idx > doc.Pages.Count Then doc.AddPages 1
        Set pg = doc.Pages(idx)
        pg.Activate
        ActiveLayer.Import files(i)
        Set sr = ActiveSelectionRange
        If sr.Count = 0 Then
            failed = failed & vbCr & FileName(files(i))
        Else
            ' page orientation follows the sheet (proof pages landscape, QA pages portrait)
            If sr.SizeWidth >= sr.SizeHeight Then
                pg.SetSize longSide, shortSide
            Else
                pg.SetSize shortSide, longSide
            End If
            ' scale proportionally to fill the page, then center it
            k = pg.SizeWidth / sr.SizeWidth
            If pg.SizeHeight / sr.SizeHeight < k Then k = pg.SizeHeight / sr.SizeHeight
            sr.SetSize sr.SizeWidth * k, sr.SizeHeight * k
            PageCenter pg, cx, cy
            sr.SetPositionEx cdrCenter, cx, cy
            SetPageName pg, PageName(files(i), i > nProof, info)
        End If
    Next i
    doc.EndCommandGroup
    doc.Pages(startIdx).Activate
    ActiveWindow.Refresh

    If failed <> "" Then MsgBox "Could not import:" & failed, vbExclamation, TITLE
    NameAndSave doc, root, n, info
    Exit Sub

ImportError:
    doc.EndCommandGroup
    MsgBox "Import stopped on " & FileName(files(i)) & ":" & vbCr & Err.Description & vbCr & vbCr & _
           "Edit > Undo removes the pages imported so far.", vbExclamation, TITLE
End Sub

Public Sub AddProofPages()
    Dim doc As Document, answer As String, total As Long, need As Long
    Dim firstNew As Long, i As Long, w As Double, h As Double

    If Documents.Count = 0 Then Set doc = CreateDocument Else Set doc = ActiveDocument
    answer = InputBox("How many pages does this proof need in total?" & vbCr & _
                      "This document has " & doc.Pages.Count & " page(s) now.", TITLE, CStr(doc.Pages.Count))
    If answer = "" Then Exit Sub
    If Not IsNumeric(answer) Then MsgBox "Please enter a number.", vbExclamation, TITLE: Exit Sub

    total = CLng(answer)
    need = total - doc.Pages.Count
    If need < 0 Then
        MsgBox "This document already has " & doc.Pages.Count & " pages." & vbCr & _
               "Delete extra pages by hand so no artwork is lost.", vbExclamation, TITLE
        Exit Sub
    End If
    doc.Unit = cdrInch
    w = doc.Pages(doc.Pages.Count).SizeWidth: h = doc.Pages(doc.Pages.Count).SizeHeight   ' match the last page
    If need > 0 Then
        firstNew = doc.Pages.Count + 1
        doc.BeginCommandGroup "Add proof pages"
        doc.AddPages need
        For i = firstNew To doc.Pages.Count
            doc.Pages(i).SetSize w, h
        Next i
        doc.EndCommandGroup
    End If
    doc.Pages(1).Activate
    MsgBox "This document now has " & doc.Pages.Count & " pages.", vbInformation, TITLE
End Sub

' ---------------------------------------------------------------------
'  file name:  Ticket# - Customer - Project.cdr   (from package_info.txt)
' ---------------------------------------------------------------------
Private Sub NameAndSave(doc As Document, ByVal root As String, ByVal nPages As Long, info As Object)
    Dim ticket As String, customer As String, subCustomer As String, project As String
    Dim folder As String, baseName As String, fullPath As String, answer As String

    ticket = info("Ticket"): customer = info("Customer"): subCustomer = info("SubCustomer"): project = info("Project")
    If ticket = "" Then ticket = InputBox("Ticket # for the file name:", TITLE)
    If customer = "" Then customer = InputBox("Customer / company name for the file name:", TITLE)
    If project = "" Then project = InputBox("Project name for the file name:", TITLE)

    ' same name the Proof Generator gave the exported files, when the package has it
    baseName = SafeName(info("FileBase"))
    If baseName = "" Or ticket <> info("Ticket") Or customer <> info("Customer") Or project <> info("Project") Then _
        baseName = JoinName(Array(ticket, customer, subCustomer, project))
    If baseName = "" Then baseName = "Proof Package"

    ' folder: the job folder from the proof (File Location) if it exists, else the unzipped package folder
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
    MsgBox "Saved:" & vbCr & answer, vbInformation, TITLE
    Exit Sub
SaveError:
    MsgBox "Could not save to:" & vbCr & answer & vbCr & vbCr & Err.Description & vbCr & _
           "Use File > Save As instead.", vbExclamation, TITLE
End Sub

' "47391", "Macon Housing Authority", "Central City" -> "47391 - Macon Housing Authority - Central City"
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
    p = Trim(p)
    If p = "" Then Exit Function
    If LCase(Right(p, 4)) = ".cdr" Or InStrRev(p, ".") > InStrRev(p, "\") Then
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
    Dim d As Object, txt As String, lines As Variant, i As Long, p As Long, st As Object, fnum As Integer
    Set d = CreateObject("Scripting.Dictionary")
    d.CompareMode = 1
    Dim k As Variant
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
Private Function PickFolder() As String
    ' Windows "Browse for Folder" window: click the unzipped package folder (or its SVG folder), then OK.
    ' The box at the bottom also accepts a pasted path.
    Dim sh As Object, fld As Object, f As String
    On Error Resume Next
    Set sh = CreateObject("Shell.Application")
    Set fld = sh.BrowseForFolder(0, "Select the unzipped proof package folder (or its SVG folder), then click OK", &H10 Or &H40 Or &H200, 0)
    If Not fld Is Nothing Then f = fld.Self.Path
    If sh Is Nothing Then f = InputBox("Paste the path of the unzipped proof package folder (or its SVG folder):", TITLE)
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

' SVG files if there are any, otherwise PNG / JPG; full paths, sorted by name
Private Function ListFiles(ByVal folder As String, files() As String) As Long
    Dim n As Long
    n = AddMatches(folder, "*.svg", files, 0)
    If n = 0 Then
        n = AddMatches(folder, "*.png", files, 0)
        n = AddMatches(folder, "*.jpg", files, n)
        n = AddMatches(folder, "*.jpeg", files, n)
    End If
    SortRange files, 1, n
    ListFiles = n
End Function

Private Function AppendFiles(ByVal folder As String, files() As String, ByVal n As Long) As Long
    Dim m As Long
    m = AddMatches(folder, "*.svg", files, n)
    SortRange files, n + 1, m
    AppendFiles = m
End Function

Private Function AddMatches(ByVal folder As String, ByVal pattern As String, files() As String, ByVal n As Long) As Long
    Dim f As String
    f = Dir(folder & pattern)
    Do While f <> ""
        n = n + 1
        ReDim Preserve files(1 To n)
        files(n) = folder & f
        f = Dir()
    Loop
    AddMatches = n
End Function

Private Sub SortRange(files() As String, ByVal a As Long, ByVal b As Long)
    Dim i As Long, j As Long, t As String
    For i = a To b - 1
        For j = i + 1 To b
            If LCase(files(j)) < LCase(files(i)) Then t = files(i): files(i) = files(j): files(j) = t
        Next j
    Next i
End Sub

' artwork on the page's own layers (master-page items such as a template logo don't count)
Private Function PageHasArt(pg As Page) As Boolean
    Dim lr As Object, isMaster As Boolean          ' late-bound: compiles even if a version lacks .Master
    For Each lr In pg.Layers
        isMaster = False
        On Error Resume Next
        isMaster = lr.Master
        On Error GoTo 0
        If Not isMaster Then
            If lr.Shapes.Count > 0 Then PageHasArt = True: Exit Function
        End If
    Next lr
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

' Page name for CorelDRAW. Files are named "Ticket - Customer - Project - p02.svg" (QA: "- qa01");
' package_info.txt lists the names (Page02=POLE SIGN 1/3, QA01=QA CHECKLIST 1/3). Older
' packages (p02_pole_sign_specs_2.svg, qa01_checklist.svg) are named from the file itself.
Private Function PageName(ByVal path As String, ByVal isQA As Boolean, info As Object) As String
    Dim s As String, key As String, num As String
    s = FileName(path)
    s = Left(s, InStrRev(s, ".") - 1)
    If LCase(s) Like "* - p##" Then
        num = Right(s, 2): key = "Page" & num
    ElseIf LCase(s) Like "* - qa##" Then
        num = Right(s, 2): key = "QA" & num
    ElseIf s Like "p##_*" Then
        key = "Page" & Mid(s, 2, 2): s = Mid(s, 5)
    ElseIf s Like "qa##_*" Then
        key = "QA" & Mid(s, 3, 2): s = "QA CHECKLIST " & CLng(Mid(s, 3, 2))
    End If
    If key <> "" And Not info Is Nothing Then
        If info.Exists(key) Then
            If info(key) <> "" Then PageName = info(key): Exit Function
        End If
    End If
    If num <> "" Then s = IIf(isQA, "QA ", "PAGE ") & CLng(num)
    PageName = UCase(Replace(s, "_", " "))
End Function
