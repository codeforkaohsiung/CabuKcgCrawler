CabuKcgCrawler
==============

A crawler for download cabu kaohsiung data.

##How to install it##
1. You must install Scrapy first. You can find how to install scrapy in [Scrapy Install Guide](http://doc.scrapy.org/en/latest/intro/install.html).
2. use git to clone this project. <br />  
    ```
    git clone https://github.com/codeforkaohsiung/CabuKcgCrawler.git
    ```
3. use follow commands to prepare to run. <br />  
    ```
    git submodule init
    git submodule update
    ```
4. you can crawel data as follow. <br />  
    ```
    scrapy list
    scrapy crawel District
    scrapy crawel 61B3
    ```
    all you crawel data will write to /data folder