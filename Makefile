init:
	pip install -r requirements.txt

run:
	python3 -m wgups

pdf:
	cd scripts && ./md2pdf.sh