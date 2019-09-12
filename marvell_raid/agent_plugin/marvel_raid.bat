@echo off
SET mvcli="C:\Program Files (x86)\Marvell\storage\interface\mvsetup.exe"
IF EXIST %mvcli% (
    echo | set /p="<<<marvell_raid_vd>>>"
    %mvcli% info -o vd
    echo | set /p="<<<marvell_raid_pd>>>"
    %mvcli% info -o pd
)