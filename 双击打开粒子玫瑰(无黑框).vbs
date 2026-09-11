Set ws = CreateObject("Wscript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(Wscript.ScriptFullName)
batPath = currentDir & "\双击打开粒子玫瑰(Windows).bat"
ws.Run chr(34) & batPath & chr(34), 0, False
