clean:
	rm -rf build project.egg-info

scrapyd:
	scrapyd

spiderkeeper:
	spiderkeeper --host=scrapyd