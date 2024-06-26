; Array Objects
Colors := "Red,Green,Blue"           ; string
ColorArray := StrSplit(Colors, ",")  ; create array

ColorArray.Push("Purple")            ; add data

for index, element in ColorArray     ; Read from the array
    MsgBox "Color " index " = " element