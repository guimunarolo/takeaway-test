run:
	docker-compose up -d

rebuild: stop
	docker-compose build

stop:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose run --rm users_api pytest -sx

clean:
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -f `find . -type f -name '@*' `
	@rm -f `find . -type f -name '#*#' `
	@rm -f `find . -type f -name '*.orig' `
	@rm -f `find . -type f -name '*.rej' `
	@rm -f .coverage
	@rm -f .env
	@rm -rf .pytest_cache
	@rm -rf coverage
	@rm -rf build
	@rm -rf htmlcov
	@rm -rf dist

ipython:
	docker-compose run --rm users_api bash -c "pip install ipython && ipython"
