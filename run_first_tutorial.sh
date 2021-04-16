# If the user is already in the netspresso-client
if [ $(basename $(pwd)) == netspresso-client ]
then
  # Get pull from Github repository
  git pull
  cd ..
  if [ -e run_first_tutorial.sh ]
  then
		rm run_first_tutorial.sh
  fi
fi

if [ ! -d netspresso-client ]
then
	# Get clone from Github repository
	git clone https://github.com/nota-github/netspresso-client
	cd netspresso-client

	# Make new venv
	python3 -m venv netspresso-venv
	source netspresso-venv/bin/activate
	pip3 install --upgrade pip

  # Insall requirermnts
	pip3 install -r requirements.txt
  
  if [ -e ../run_first_tutorial.sh ]
  then
		rm ../run_first_tutorial.sh
  fi

else
	cd netspresso-client
  source netspresso-venv/bin/activate
fi

# Run the first tutorial
python3 netspresso_cli/main.py --config config_files/tutorial_0.yml
