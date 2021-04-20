@ECHO off
REM SET currentFolder=for %%* in (.) do @echo %%~n*
set knownfile=%cd%

for /F "delims=\ tokens=2" %%G in ("%knownfile%") do (
    set prev=.\%%G
)

REM ECHO %prev%

if %prev% == "netspresso-client" (
REM Get pull from Github repository
  git pull
  cd ..
  
REM  if  exist "win_run_first_tutorial.bat" (
REM	  del "win_run_first_tutorial.bat"
REM    )
)

if  not exist "netspresso-client" (
REM Get clone from Github repository
	git clone https://github.com/nota-github/netspresso-client -b develop
	cd "netspresso-client"
    

REM Make new venv
	python3 -m venv --system-site-packages "netspresso-venv" 
	call netspresso-venv/scripts/activate
	pip3 install --upgrade pip

REM Insall requirements
	pip3 install --user -r requirements.txt
  
REM  	if  exist "../win_run_first_tutorial.bat" ( 
REM		del "../win_run_first_tutorial.bat"
REM	)
  
) else (
	cd "netspresso-client"
  call netspresso-venv/scripts/activate
)
REM Run the first tutorial
python3 netspresso_cli/main.py --config config_files/tutorial_0.yml