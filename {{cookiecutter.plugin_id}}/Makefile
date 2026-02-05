.PHONY: build dev help install patch minor major release tags lint lint-fix format format-check check
{% if cookiecutter.enable_vitest == "yes" %}
.PHONY: test coverage
{% endif %}

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make build        - Build the plugin for production"
	@echo "  make dev          - Build and watch for changes"
	@echo "  make lint         - Check code style with ESLint"
	@echo "  make lint-fix     - Fix code style issues automatically"
	@echo "  make format       - Format code with Prettier"
	@echo "  make format-check - Check code formatting"
	@echo "  make check        - Run lint and format checks"
{% if cookiecutter.enable_vitest == "yes" %}
	@echo "  make test         - Run tests"
	@echo "  make coverage     - Run tests with coverage report"
{% endif %}
	@echo "  make patch        - Bump patch version (0.0.x)"
	@echo "  make minor        - Bump minor version (0.x.0)"
	@echo "  make major        - Bump major version (x.0.0)"
	@echo "  make release      - Push commits and tags to remote"
	@echo "  make tags         - List git tags"

install:
	npm install

build:
	npm run build

dev:
	npm run dev

lint:
	npm run lint

lint-fix:
	npm run lint -- --fix

format:
	npm run format

format-check:
	npm run format:check

check:
	npm run check

{% if cookiecutter.enable_vitest == "yes" %}
test:
	npm run test

coverage:
	npm run test:coverage
{% endif %}

patch: check
	npm version patch

minor: check
	npm version minor

major: check
	npm version major

release: {% if cookiecutter.enable_vitest == "yes" %}test {% endif %}check
	git push origin HEAD --follow-tags

tags:
	git tag --list
