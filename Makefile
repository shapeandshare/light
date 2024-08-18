
setup:
	resources/setup.sh

prepare:
	resources/prepare.sh

clean:
	rm -rf ./build ./dist ./src/shapeandshare.light.egg-info

nuke:
	rm -rf ./build ./dist ./src/shapeandshare.light.egg-info ./venv ./data tests/integration/venv tests/integration/data tests/integration/shapeandshare.light*.whl

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

client:
	resources/client.sh

integration:
	make nuke
	make setup
	make prepare
	make build
	cd tests/integration/ && make nuke
	cp dist/shapeandshare.light-*.whl tests/integration/
	cd tests/integration/ && make setup
	cd tests/integration/ && make prepare
	cd tests/integration/ && make server
	cd tests/integration/ && make client
