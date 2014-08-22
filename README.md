CabuKcgCrawler
==============

A crawler for download cabu kaohsiung data.

##How to install it##
* You must install Scrapy first. You can find how to install scrapy in [Scrapy Install Guide](http://doc.scrapy.org/en/latest/intro/install.html).
* use git to clone this project.

	```bash
	git clone https://github.com/codeforkaohsiung/CabuKcgCrawler.git
	```

* use follow commands to prepare to run.
 
	```bash
	git submodule init
	git submodule update
	```

* you can crawel data as follow. all you crawel data will write to /data folder

	```bash
	scrapy list
	scrapy crawel District
	scrapy crawel 61B3
	```
