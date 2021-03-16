@echo off
chcp 65001
set work_path=%cd%
for /r %work_path% %%i in (*.srt) do (
	echo %%i >> raw.txt
	type %%i >> raw.txt
	)
pause