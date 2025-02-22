@echo Start registering
if exist "C:\Windows\SysWOW64\vcruntime140d.dll" ( 
	@echo vcruntime140d.dll already exists
) else ( 
	copy vcruntime140d.dll %windir%\SysWOW64\
	regsvr32 %windir%\SysWOW64\vcruntime140d.dll /s
	@echo vcruntime140d.dll registration is successful
)


if exist "C:\Windows\SysWOW64\ucrtbased.dll" ( 
	@echo ucrtbased.dll already exists
) else ( 
	copy ucrtbased.dll %windir%\SysWOW64\
	regsvr32 %windir%\SysWOW64\ucrtbased.dll /s
	@echo ucrtbased.dll registration is successful
)

if exist "C:\Windows\SysWOW64\RsVisa32.dll" ( 
	@echo RsVisa32.dll already exists
) else ( 
	copy RsVisa32.dll %windir%\SysWOW64\
	regsvr32 %windir%\SysWOW64\RsVisa32.dll /s
	@echo RsVisa32.dll registration is successful
)

if exist "C:\Windows\SysWOW64\visa32.dll" ( 
	@echo visa32.dll already exists
) else ( 
	copy visa32.dll %windir%\SysWOW64\
	regsvr32 %windir%\SysWOW64\visa32.dll /s
	@echo visa32.dll registration is successful
)

if exist "C:\Windows\SysWOW64\kernel32.dll" ( 
	@echo kernel32.dll already exists
) else ( 
	copy kernel32.dll %windir%\SysWOW64\
	regsvr32 %windir%\SysWOW64\kernel32.dll /s
	@echo kernel32.dll registration is successful
)

@echo The files has been registered successfully

@pause