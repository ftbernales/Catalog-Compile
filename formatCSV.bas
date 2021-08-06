Attribute VB_Name = "formatCSV"
Sub formatOverallSeismicityCSV()
Application.ScreenUpdating = False
N_events = Application.CountA(Range("A:A")) - 1

'1
Range("B:G").EntireColumn.Insert

'2, 3
headers = Array("year", "month", "day", "hour", "minute", "second")
formulas = Array("=NUMBERVALUE(LEFT(A2,4))", "=NUMBERVALUE(MID(A2,6,2))", "=NUMBERVALUE(MID(A2,9,2))", "=NUMBERVALUE(MID(A2,12,2))", "=NUMBERVALUE(MID(A2,15,2))", "=NUMBERVALUE(MID(A2,18,6))")
For i = 0 To 5
    Cells(1, i + 2).Value = headers(i)
    Cells(2, i + 2).Formula = formulas(i)
Next i
ActiveSheet.Calculate

'4
Range(Cells(2, 2), Cells(N_events + 1, 7)).FillDown
Range(Cells(2, 2), Cells(N_events + 1, 7)).Value = Range(Cells(2, 2), Cells(N_events + 1, 7)).Value

'5
Range("M:O").EntireColumn.Insert

'6, 7
headers2 = Array("ctgry", "Ms", "Mw")
formulas2 = Array("=IF(L2=" & Chr(34) & "mb" & Chr(34) & ", 1, IF(L2=" & Chr(34) & "ms" & Chr(34) & ", 2, 0))", "=IF(M2=0, " & Chr(34) & "n.a." & Chr(34) & ", IF(M2=2, K2, IF(M2=1, (10.29-(3.55*K2)+(0.48*K2*K2)), " & Chr(34) & "" & Chr(34) & ")))", "=IF(N2=" & Chr(34) & "n.a." & Chr(34) & ", K2, IF(AND(N2>=3, N2<=6.1,J2<70), ((0.67*N2)+2.12), IF(AND(N2>=6.2, N2<=8.4, J2<70), ((1.06*N2)-0.38), IF(AND(N2>=3.3, N2<=7.2, J2>=70, J2<=678), ((0.67*N2)+2.33), " & Chr(34) & "" & Chr(34) & "))))")
For i = 0 To 2
    Cells(1, i + 13).Value = headers2(i)
    Cells(2, i + 13).Formula = formulas2(i)
Next i
ActiveSheet.Calculate

'8, 9
Range(Cells(2, 13), Cells(N_events + 1, 15)).FillDown
Range(Cells(2, 13), Cells(N_events + 1, 15)).Value = Range(Cells(2, 13), Cells(N_events + 1, 15)).Value

'10 - 12
Range("A1").Value = "eventID"
For i = 0 To N_events - 1
    Cells(i + 2, 1).Value = i + 1
Next i

'13
Range(Cells(1, 30), Cells(N_events + 1, 30)).Cut
Range("B1").Insert Shift:=xlToRight

'14
Range(Cells(1, 10), Cells(N_events + 1, 10)).Cut
Range("I1").Insert Shift:=xlToRight

'15
Range("I:I").EntireColumn.Insert

'16
Range("L:N").EntireColumn.Insert

'17
Range(Cells(1, 31), Cells(N_events + 1, 31)).Cut
Range("P1").Insert Shift:=xlToRight

'18
Range("Q:T").Delete

'19
Range(Cells(1, 28), Cells(N_events + 1, 28)).Cut
Range("R1").Insert Shift:=xlToRight

'20
Range("S:AE").Delete

'21
newHeaders = Array("eventID", "Agency", "year", "month", "day", "hour", "minute", "second", "timeError", "longitude", "latitude", "SemiMajor90", "SemiMinor90", "ErrorStrike", "depth", "depthError", "magnitude", "sigmaMagnitude")
For i = 0 To UBound(newHeaders)
    Cells(1, i + 1).Value = newHeaders(i)
Next i

'22
ActiveSheet.SaveAs ActiveWorkbook.Path & "\Overall_Seismicity_Formatted_" & Year(Date) & "." & Format(Month(Date), "00") & "." & Format(Day(Date), "00") & ".csv", xlCSV
End Sub

