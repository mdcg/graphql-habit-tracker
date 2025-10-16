runserver:
	python -m application.api

code-quality/format:
	unimport -r application domain infrastructure
	isort application domain infrastructure
	black application domain infrastructure
