@echo off
REM If the user is already in the netspresso-client

if basename "$PWD" == netspresso-client (
REM Get pull from Github repository
  git pull
  cd ..
  )
  if  exist "run_first_tutorial.sh" (
	  del "run_first_tutorial.sh"
    )

if  not exist "netspresso-client" (
REM Get clone from Github repository
	git clone https://github.com/nota-github/netspresso-client -b develop
	cd "netspresso-client"
    )

REM Make new venv
	python3 -m venv "netspresso-venv"
	source "netspresso-venv/bin/activate"
	pip3 install --upgrade pip

REM Insall requirermnts
	pip3 install -r requirements.txt
  
  if  exist "../run_first_tutorial.sh" 
		del "../run_first_tutorial.sh"
  else
	cd "netspresso-client"
  source netspresso-venv/bin/activate

REM Run the first tutorial
python3 netspresso_cli/main.py --config config_files/tutorial_0.yml