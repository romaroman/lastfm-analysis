analyze:
	python src/main.py

clear_results:
	rm -r dumps/* && rm -r maps/*

clear_cache:
	rm -r .pytest_cache && find . -name "*.pyc" -exec rm -f {} \

sample:
	python src/main.py -u username -l 20

install_reqs:
	python -m pip install -r requirements.txt

start_bot:
	python src/bot.py

build_image:
	docker build -t lastfm_analysis .