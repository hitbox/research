-- Generate cats random names
INSERT INTO cats (cat_name)
WITH
hon AS (
    SELECT *
    FROM unnest(ARRAY['mr', 'ms', 'miss', 'doctor', 'frau', 'fraulein', 'missus', 'governer']) WITH ORDINALITY AS hon(n, i)
),
fn AS (
    SELECT *
    FROM unnest(ARRAY['flopsy', 'mopsey', 'whisper', 'fluffer', 'tigger', 'softly']) WITH ORDINALITY AS fn(n, i)
),
mn AS (
    SELECT *
    FROM unnest(ARRAY['biggles', 'wiggly', 'mossturn', 'leaflittle', 'flower', 'nonsuch']) WITH ORDINALITY AS mn(n, i)
),
ln AS (
    SELECT *
    FROM unnest(ARRAY['smithe-higgens', 'maclarter', 'ipswich', 'essex-howe', 'glumfort', 'pigeod']) WITH ORDINALITY AS ln(n, i)
)
SELECT initcap(concat_ws(' ', hon.n, fn.n, mn.n, ln.n)) AS name
FROM hon, fn, mn, ln, generate_series(1,1000)
ORDER BY random();

-- Fill in the tag names
INSERT INTO tags (tag_name) VALUES
    ('soft'), ('cuddly'), ('brown'), ('red'), ('scratches'), ('hisses'), ('friendly'), ('aloof'), ('hungry'), ('birder'), ('mouser');

-- Generate random tagging. Every cat has 25% chance of getting each tag.
INSERT INTO cat_tags
WITH tag_ids AS (
    SELECT DISTINCT tag_id FROM tags
),
tag_count AS (
    SELECT Count(*) AS c FROM tags
)
SELECT cat_id, tag_id
FROM cats, tag_ids, tag_count
WHERE random() < 0.25;

CREATE INDEX cat_tags_x ON cat_tags (tag_id);
