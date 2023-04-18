-- Active: 1681832541458@@baza.fmf.uni-lj.si@5432@sem2023_tinef@public

CREATE TABLE funkcije (
    naziv text not null primary key
);

Create table cin (
    cin text not null primary key
);

CREATE TABLE clani (
    emso integer primary key,
    ime text not null, 
    priimek text not null,
    funkcija text not null REFERENCES funkcije(naziv), 
    cin text not null REFERENCES cin(cin)
);

create table tip_vozila (
    tip_vozila text not null PRIMARY KEY
);

create table kategorija_vozniskega_dovoljenja (
    kategorija text not null PRIMARY KEY
);

create table vozila (
    registrska_st text not null PRIMARY KEY,
    tip_vozila text not null REFERENCES tip_vozila(tip_vozila),
    potreben_izpit text not null REFERENCES kategorija_vozniskega_dovoljenja(kategorija),
    st_potnikov INTEGER NOT NULL
);

create table tip_intervencije (
    tip text not null primary key
);

CREATE TABLE intervencija (
    id Serial PRIMARY KEY,
    opis TEXT,
    datum date not null,
    tip text not null REFERENCES tip_intervencije(tip)
);

create Table osebna_oprema (
    id Serial PRIMARY KEY,
    tip_opreme text not null
);

create table skupna_oprema (
    id Serial PRIMARY KEY,
    tip_opreme text not null
);

create table tecaji (
    id Serial PRIMARY KEY,
    naziv_tecaja text not null,
    datum date not null, 
    organizator text not null, 
    cena FLOAT
);

create table vaja (
    id Serial PRIMARY KEY,
    datum date not null, 
    obvezna BOOLEAN not null, 
    tip_vaje text not null REFERENCES tip_intervencije(tip), 
    vodja integer REFERENCES clani(emso)
);

create table tipi_tekmovanj (
    tip text not null PRIMARY KEY
);

create table tekmovanje (
    id serial PRIMARY key, 
    datum date not null, 
    lokacija text not null, 
    tip_tekmovanja text not null REFERENCES tipi_tekmovanj(tip)
);

create table ekipa (
    id serial PRIMARY key
);

create table tehnicni_pregledi_vozil (
    id serial PRIMARY key,
    vozilo text not null REFERENCES vozila(registrska_st),
    datum date not null
);