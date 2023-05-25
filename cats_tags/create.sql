CREATE TABLE cats (
    cat_id serial primary key,
    cat_name text not null
);

CREATE TABLE cat_tags (
    cat_id integer not null,
    tag_id integer not null,
    unique(cat_id, tag_id)
);

CREATE TABLE tags (
    tag_id serial primary key,
    tag_name text not null,
    unique(tag_name)
);
