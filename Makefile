name?=ticks.egg

clean:
	rm -rf build project.egg-info

scrapyd:
	scrapyd

spiderkeeper:
	spiderkeeper --host=scrapyd

deploy:
	scrapyd-deploy --build-egg $(name)
