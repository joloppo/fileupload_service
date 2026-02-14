_default:
    @just --list

set dotenv-load := true
alias t := test

dev:
    uv run uvicorn fileupload_service.app:app --reload

test:
    uv run pytest tests