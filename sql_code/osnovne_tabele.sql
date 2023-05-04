-- Active: 1681832541458@@baza.fmf.uni-lj.si@5432@sem2023_tinef@public
CREATE TABLE funkcija (
    id_funkcija serial PRIMARY KEY, 
    naziv text not null
);

Create table cin (
    id_cin serial PRIMARY KEY, 
    cin text not null
);

CREATE TABLE clan (
    emso integer primary key,
    ime text not null, 
    priimek text not null,
    funkcija integer not null REFERENCES funkcija(id_funkcija), 
    cin integer not null REFERENCES cin(id_cin)
);

create table tip_vozila (
    id_vozilo serial PRIMARY KEY, 
    tip_vozila text not null
);

create table kategorija_vozniskega_dovoljenja (
    id_kategorije serial PRIMARY KEY,
    kategorija text not null
);

create table vozilo (
    registrska_st text not null PRIMARY KEY,
    tip_vozila integer not null REFERENCES tip_vozila(id_vozilo),
    potreben_izpit text not null REFERENCES kategorija_vozniskega_dovoljenja(id_kategorije),
    st_potnikov INTEGER NOT NULL
);

create table tip_intervencije (
    id_tipa_intervencije serial PRIMARY KEY, 
    tip text not null
);

CREATE TABLE intervencija (
    id Serial PRIMARY KEY,
    opis TEXT,
    datum date not null,
    tip integer not null REFERENCES tip_intervencije(id_tipa_intervencije)
);

create Table osebna_oprema (
    id Serial PRIMARY KEY,
    tip_opreme text not null
);

create table skupna_oprema (
    id Serial PRIMARY KEY,
    tip_opreme text not null
);

create table tip_tecaja (
    id_tecaj serial PRIMARY KEY, 
    naziv_tecaja text not null 
);

create table tecaj (
    id Serial PRIMARY KEY,
    naziv_tecaja INTEGER not null REFERENCES tip_tecaja(id_tecaj),
    datum date not null, 
    organizator text not null, 
    cena FLOAT
);

create table vaja (
    id Serial PRIMARY KEY,
    datum date not null, 
    obvezna BOOLEAN not null, 
    tip_vaje INTEGER not null REFERENCES tip_intervencije(id_tipa_intervencije), 
    vodja integer REFERENCES clan(emso)
);

create table tip_tekmovanja (
    id_tip serial PRIMARY KEY, 
    tip text not null
);

create table tekmovanje (
    id serial PRIMARY key, 
    datum date not null, 
    lokacija text not null, 
    tip_tekmovanja INTEGER not null REFERENCES tip_tekmovanja(id_tip)
);

create table ekipa (
    id serial PRIMARY key
);

create table tehnicni_pregledi_vozil (
    id serial PRIMARY key,
    vozilo text not null REFERENCES vozilo(registrska_st),
    datum date not null
);