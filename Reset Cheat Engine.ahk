#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#WinActivateForce
DetectHiddenWindows, on
DetectHiddenText, on

^r::
	Process, Close, pcsx2.exe

	; !! put your path here to PCSX2 installation !!
	Run "C:\Program Files (x86)\PCSX2 1.4.0\pcsx2-v1.5.0-dev-1739-g7aa554b-windows-x86\pcsx2.exe"


	; !! name of PCSX2 window here !!
	EmuWindow := "PCSX2 v1.5.0-dev-1739-g7aa554b"
	
	WinWait, %EmuWindow%, , 2
	if ErrorLevel
		MsgBox PCSX2 Taking too long to open.
		
	else {
		; you should already have cheat engine open
		; open the iso
		WinMenuSelectItem, %EmuWindow%, , System, Boot ISO (fast)
		
		; once game is opened
		WinWait, Slot, , 2
		if ErrorLevel
			MsgBox Taking too long to boot ISO.
			
		else 
		{
			;press F3 to reload save state
			Send {F3}
			
			IfWinExist, Cheat Engine 6.4
			{
				; move to cheat engine window
				WinActivate, Cheat Engine
				
				; open process menu because my god what the hell
				Send, ^p
			
				; click open, cheat engine should still select pcsx2
				; make sure your last selected option was "Open"
				Send {Enter}
				; if using existing address list, preserve its
				WinWait, Confirmation, , 2
				if !ErrorLevel 
					Send {Enter}
			}
			else 
			{
				MsgBox Open Cheat Engine and Try Again
				Return
			}
		}
	}
	Return
