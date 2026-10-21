
install:
	@uv sync

run :
	@uv run python3 -m src

clean: 
	@find . -name "__pycache__" -exec rm -rf {} +
