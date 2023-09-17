create database demo_gpdb;
create extension if not exists vector;
\c demo_gpdb;
set optimizer to off;
create table audio_embeddings(index int, ids text, panns_embeddings vector(2048), audio  double precision[]);
create table audio_metadata(index bigint, ids text, artist text, genre text, name text, subgenres text, urls text);
create table public.audio (index bigint, ids text, artist text, genre text, name text, subgenres text, urls text, audio double precision[], panns_embeddings vector(2048));
insert into audio select a.*, b.audio, b.panns_embeddings from audio_embeddings b left join audio_metadata a on b.ids = a.ids;
copy public.audio from '/home/gpadmin/audio.csv' CSV HEADER DELIMITER '|' QUOTE '"' NULL '';  
