GPU_IMAGE?="tensortrade:latest-gpu"
CPU_IMAGE?="tensortrade:latest"

clean:
	find . | grep -E '(__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf

test:
	pytest tests/

test-parallel:
	pytest --workers auto tests/

doctest:
	pytest --doctest-modules tensortrade/

docs-build:
	$(MAKE) -C docs html

docs-clean:
	$(MAKE) -C docs clean
	rm -rf docs/source/api

docs-serve:
	$(SHELL) -C cd docs/build/html
	python3 -m webbrowser http://localhost:8000/docs/build/html/index.html
	python3 -m http.server 8000

build-cpu: 
	docker build -t ${CPU_IMAGE} .

build-cpu-if-not-built: 
	if [ ! $$(docker images -q ${CPU_IMAGE}) ]; then $(MAKE) build-cpu; fi;

build-gpu:
	docker build -t ${GPU_IMAGE} . --build-arg gpu_tag="-gpu"

run-notebook:
	$(MAKE) build-cpu-if-not-built
	docker run -it --rm -p=8888:8888 ${CPU_IMAGE} jupyter notebook --ip='*' --port=8888 --no-browser --allow-root /examples/

run-docs: 
	$(MAKE) build-cpu-if-not-built
	if [ $$(docker ps -aq --filter name=tensortrade_docs) ]; then docker rm $$(docker ps -aq --filter name=tensortrade_docs); fi;
	docker run -t --name tensortrade_docs ${CPU_IMAGE} make docs-build
	docker cp tensortrade_docs:/docs/. ./docs/
	docker container rm tensortrade_docs

run-test: 
	$(MAKE) build-cpu-if-not-built
	docker run -it --rm ${CPU_IMAGE} make test

package:
	rm -rf dist
	python3 setup.py sdist
	python3 setup.py bdist_wheel

test-release: package
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: package
	twine upload dist/*
