if [ $(basename $(pwd)) == netspresso-client ]
then
  # Get pull from Github repository
  git pull
  cd ..
  # echo $(basename $(pwd))
fi

if [ ! -d netspresso-client ]
then
	# Get clone from Github repository
	git clone https://github.com/nota-github/netspresso-client
	cd netspresso-client

	# Make new venv
  if [ ! -d netspresso-venv ]
  then
		python3 -m venv netspresso-venv
		source netspresso-venv/bin/activate
		pip3 install --upgrade pip
  else
	  source netspresso-venv/bin/activate
  fi

  # Insall requirermnts
	pip3 install -r requirements.txt
else
	cd netspresso-client
  source netspresso-venv/bin/activate
fi

# Run the first tutorial
python3 netspresso_cli/main.py --config config_files/tutorial_0.yml
