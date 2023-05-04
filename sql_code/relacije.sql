-- Active: 1681832541458@@baza.fmf.uni-lj.si@5432@sem2023_tinef@public
create table opravljeni_tecaji (
    id serial primary KEY, 
    id_tecaja integer not null REFERENCES tecaj(id),
    emso_udelezenca integer not null REFERENCES clan(emso)
);

create table del_ekipe (
    id serial PRIMARY KEY, 
    id_ekipe integer not null REFERENCES ekipa(id), 
    emso_clana integer not null REFERENCES clan(emso)
);

create table prisotnost_na_intervencijah (
    id serial PRIMARY key, 
    id_intervencije integer not null REFERENCES intervencija(id), 
    emso_prisotnega integer not null REFERENCES clan(emso)
);

create table prisotnost_na_vajah (
    id serial PRIMARY key, 
    id_vaje integer not null REFERENCES vaja(id), 
    emso_prisotnega integer not null REFERENCES clan(emso)
);

create table vozila_na_intervencijah (
    id serial PRIMARY key, 
    id_intervencije integer not null REFERENCES intervencija(id), 
    registracija_vozila text not null REFERENCES vozilo(registrska_st)
);

create table ekipe_na_tekmovanjih (
    id serial PRIMARY key, 
    id_tekmovanja integer not null REFERENCES tekmovanje(id), 
    id_ekipe integer not null REFERENCES ekipa(id),
    rezultat_opis text not null
);

create table lastnistva_opreme (
    id serial PRIMARY KEY,
    id_lastnika integer REFERENCES clan(emso) DEFAULT 0,
    tip_opreme integer not null REFERENCES osebna_oprema(id), 
    velikost text,
    stevilo integer
);

create table oprema_v_vozilih (
    id serial PRIMARY KEY,
    registracija_vozila text REFERENCES vozila(registrska_st) DEFAULT 0,
    tip_opreme integer not null REFERENCES skupna_oprema(id), 
    dodatne_informacije text
);

create table potrebuje_tecaj (
    id serial PRIMARY KEY,
    id_opreme integer not null REFERENCES skupna_oprema(id),
    id_tecaja integer not null REFERENCES tecaj(id)
);

create table skrbnik_vozila (
    id SERIAL PRIMARY KEY, 
    emso_clana integer not null REFERENCES clan(emso), 
    registracija_vozila text not null REFERENCES vozilo(registrska_st)
);