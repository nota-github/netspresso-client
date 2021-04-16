if [ ! -d netspresso-client ]
then
	# Get clone from Github repository
	git clone https://github.com/nota-github/netspresso-client
	cd netspresso-client

	# Make new venv
	python3 -m venv netspresso-venv
	source netspresso-venv/bin/activate
	pip install --upgrade pip
fi


# Insall requirermnts
pip install -r requirements.txt

# Run the first tutorial
python3 netspresso_cli/main.py --config config_files/tutorial_0.yml
