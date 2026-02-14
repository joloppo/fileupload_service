_default:
    @just --list

set dotenv-load := true
alias t := test

dev:
    uv run uvicorn fileupload_service.app:build_app --reload

test:
    uv run pytest tests

docker-up:
    docker build -t file-upload-service . \
      && docker run -d -p 8000:8000 --name file-upload-container file-upload-service

docker-down:
    docker stop file-upload-container \
      && docker rm file-upload-container
