CREATE TABLE IF NOT EXISTS wiki_updates (
	id 	serial,
	added_date	timestamp primary key,
    total_edit int,
    de_wiki int )
;


CREATE OR REPLACE FUNCTION trg_wiki_updates_partition()
    RETURNS trigger AS
$func$
DECLARE
    _tbl text := to_char(NEW.added_date, '"wiki_updates_y"IYYY_"w"IW');
    _rec_date date := NEW.added_date::date;
    _min_date date := date_trunc('week', NEW.added_date)::date;
    _max_date date := date_trunc('week', NEW.added_date)::date + 7;
    _min_live date := date_trunc('week', NEW.added_date)::date - 1;
BEGIN
IF NOT EXISTS (
    SELECT 1
    FROM   pg_catalog.pg_class c
    JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE  n.nspname = 'public'
    AND    c.relname = _tbl
    AND    c.relkind = 'r') THEN
    EXECUTE format('CREATE TABLE IF NOT EXISTS %I
                    (CHECK (added_date::date >= to_date(%L, ''yyyy-mm-dd'') AND
                            added_date::date <  to_date(%L, ''yyyy-mm-dd'')),
                        LIKE wiki_updates INCLUDING INDEXES )
                        INHERITS (wiki_updates)'
            , _tbl
            , to_char(_min_date, 'YYYY-MM-DD')
            , to_char(_max_date, 'YYYY-MM-DD')
            );
END IF;
EXECUTE 'INSERT INTO ' || quote_ident(_tbl) || ' VALUES ($1.*)'
USING NEW;
RETURN NULL;
END
$func$ LANGUAGE plpgsql SET search_path = public;


DROP TRIGGER IF EXISTS ins_wiki_updates on wiki_updates;
CREATE TRIGGER ins_wiki_updates
BEFORE INSERT ON wiki_updates
FOR EACH ROW EXECUTE PROCEDURE trg_wiki_updates_partition();