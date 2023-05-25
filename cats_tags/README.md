https://www.crunchydata.com/blog/tags-aand-postgres-arrays-a-purrfect-combination

I don't understand why he just doesn't do this:

```sql
SELECT count(*)
  FROM cats
  JOIN cat_tags
    ON cats.cat_id = cat_tags.cat_id
  JOIN tags
    ON cat_tags.tag_id = tags.tag_id
 WHERE tags.tag_name in ('red', 'brown', 'aloof');
```
