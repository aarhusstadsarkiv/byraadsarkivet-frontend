BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "meetings" (
  "id" INTEGER,
  "fora_id" INTEGER NOT NULL,
  "fora_name" TEXT NOT NULL,
  "year" INTEGER NOT NULL,
  "date" TEXT NOT NULL,
  "title" TEXT,
  "public" BOOLEAN,
  "agenda" JSON,
  "metadata" JSON,
  "files" JSON,
  PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "cases" (
  "id" INTEGER,
  "db_id" INTEGER NOT NULL,
  "type" TEXT,
  "title" TEXT,
  "public" BOOLEAN,
  "date" TEXT NOT NULL,
  "last_deliberation_date" TEXT NOT NULL,
  "year" INTEGER NOT NULL,
  "subtitle" TEXT,
  "resume" TEXT,
  "suggestion" TEXT,
  "presentation" TEXT,
  "notes" TEXT,
  "fora" TEXT,
  "decisions" JSON,
  "files" JSON,
  "metadata" JSON,
  PRIMARY KEY("id")
);

CREATE VIRTUAL TABLE "cases_fts" USING FTS5(
  title,
  subtitle,
  resume,
  suggestion,
  presentation,
  notes,
  detail = full,
  content_rowid = 'id',
  content = 'cases',
  -- This syntax works!
  tokenize="unicode61 remove_diacritics 2 tokenchars '-_'"
);

CREATE TRIGGER after_cases_insert
AFTER
INSERT ON cases BEGIN
INSERT INTO cases_fts (
    rowid,
    title,
    subtitle,
    resume,
    suggestion,
    presentation,
    notes
  )
VALUES
  (
    new.id,
    new.title,
    new.subtitle,
    new.resume,
    new.suggestion,
    new.presentation,
    new.notes
  );
END;
COMMIT;
