# FastAPI Fileuploader

# How to use (using [justfile](https://github.com/casey/just?tab=readme-ov-file#cross-platform)):
 - `just dev` -> this starts the api locally
 - `just docker-up` -> starts the api in docker, locally, access using localhost:8000
 - `just docker-down` -> stops the docker container & removes it
 - 'just test' -> runs tests

# Things I didn't do that I would do:
 - Add tests
 - MAP Project Errors to HTTP Errors [!!!NB], might do it in a minute
 - Put chunking settings & deploy settings in correct places (e.g. not hard coded in the code)
 - Limit id length, but not sure what id is supposed to be anyway
 - Could add more metadata to StoredFileInfo, like content type, size etc
 - Carry over file name to download (instead of id) (what is id?!)
 - Handle files with the same content but different ids/names - currently raises
 - Decide whether file_id should be a query parameter or part of the path - if part of path 404 would make more sense
 - Separate project errors and http errors, map them explicitly
 - Add more docs and example values into fastapi -> swagger

# If one were to deploy this
 - Add health endpoints for deployment
 - Metrics, telemetry etc.