
all:
	python3 insert.py

init:
	cp -f heal2u/* . 
	git clone https://github.com/heal2u/heal2u.github.io.git

update:
	cd heal2u.github.io; git pull
	python3 statistics.py  
	python3 year_statistics.py
	cp -f month.yaml heal2u.github.io/_data
	cp -f year.json heal2u.github.io/data
	cd heal2u.github.io; git diff; git commit -a -m "update data" ; git push

percent:
	python3 year_statistics.py
