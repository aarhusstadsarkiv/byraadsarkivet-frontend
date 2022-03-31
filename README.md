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

## Columns
1. Cases
id,db_id,type,title,public,date,last_deliberation_date,year,subtitle,resume,suggestion,presentation,notes,fora,decisions,files,metadata

2. Meetings
id,fora_id,fora_name,year,date,title,public,agenda,metadata,files

## Batch update (with FirstAgenda data)
1. `$ python import_new_cases_to_db.py`
2. `$ python import_new_meetings_to_db.py`
3. Run workflow to generate new .db from the new csv-files

## Generate new .db-file from updated csv-files
- `$ sqlite3`
- `$ sqlite> .open db.db`
- `$ sqlite> .read schema.sql`
- `$ sqlite> .mode csv`
- `$ sqlite> .import data/merged_cases.csv cases`
- `$ sqlite> .import data/merged_meetings.csv meetings`
- `$ sqlite> .quit`

## Singular update
Used when a citizen has asked for personal data to be removed.
This fires a complete update of one or more cases or meetings, and a replacement of one or more files.

1. get the id of the relevant meeting or case.
2. get the relevant data via the json-api
3. update the case-dict if necessary
4. replace any binary files with the redacted copies
