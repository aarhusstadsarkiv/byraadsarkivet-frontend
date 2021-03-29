# Byraadsarkivet
Front for byraadsarkivet.

## Online sites
- Production site:
  https://byraadsarkivet.aarhus.dk
- Test site:
  https://minutes-aar-test.azurewebsites.net (currently not active)

### Local test:
`$ datasette -i db.db --reload --plugins-dir plugins/ --template-dir templates/ --static static:static/ --metadata metadata.json --setting template_debug 1`

### Docker test
1. `$ docker build . --tag minutes.azurecr.io/aar-{current_date}-v{version}`
2. `$ docker run -p 80:80 minutes.azurecr.io/aar-{current_date}-v{version}`

### Docker deployment
3. `$ docker login minutes.azurecr.io`
4. `$ docker push minutes.azurecr.io/aar-{current_date}-v{version}`
5. `$ docker stop {container-name}`

### Azure deployment
1. Update docker image for either minutes-aar or minutes-aar-test

## Performance
Use locust to performance test the online frontend from /tests:
`$ locust --config=config.conf`

## Singular update
Used when a citizen has asked for personal data to be removed.
This fires a complete update of one or more cases or meetings, and a replacement of one or more files.

1. get the id of the relevant meeting or case.
2. get the relevant data via the json-api
3. update the case-dict if necessary
4. replace any binary files with the redacted copies
