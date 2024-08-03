
setup:
	resources/setup.sh

prepare:
	resources/prepare.sh

clean:
	rm -rf ./build ./dist ./src/shapeandshare.light.egg-info

nuke:
	rm -rf ./build ./dist ./src/shapeandshare.light.egg-info ./venv ./data

build:
	resources/build.sh

publish:
	resources/publish.sh

lint:
	resources/lint.sh

lint-fix:
	resources/lint-fix.sh

server:
	resources/server.sh
