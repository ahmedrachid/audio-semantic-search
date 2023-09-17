create database demo_gpdb;
\c demo_gpdb;
set optimizer to off;
create table public.audio (index bigint, ids text, artist text, genre text, name text, subgenres text, urls text, audio double precision[], panns_embeddings vector(2048));
copy public.audio from '/home/gpadmin/audio.csv' CSV HEADER DELIMITER '|' QUOTE '"' NULL '';  
