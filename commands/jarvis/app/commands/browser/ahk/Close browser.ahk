GroupAdd("browsers", "ahk_class MozillaWindowClass")
GroupAdd("browsers", "ahk_class IEFrame")
GroupAdd("browsers", "ahk_exe msedge.exe")
GroupAdd("browsers", "ahk_exe chrome.exe")
GroupAdd("browsers", "ahk_exe firefox.exe")
GroupAdd("browsers", "ahk_exe browser.exe")

WinClose("ahk_group browsers")