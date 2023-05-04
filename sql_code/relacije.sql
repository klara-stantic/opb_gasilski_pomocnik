-- Active: 1681832541458@@baza.fmf.uni-lj.si@5432@sem2023_tinef@public
CREATE TABLE opravljeni_tecaji (
    id SERIAL PRIMARY KEY, 
    id_tecaja INTEGER NOT NULL REFERENCES tecaj(id),
    emso_udelezenca INTEGER NOT NULL REFERENCES clan(emso)
);

CREATE TABLE del_ekipe (
    id SERIAL PRIMARY KEY, 
    id_ekipe INTEGER NOT NULL REFERENCES ekipa(id), 
    emso_clana INTEGER NOT NULL REFERENCES clan(emso)
);

CREATE TABLE prisotnost_na_intervencijah (
    id SERIAL PRIMARY KEY, 
    id_intervencije INTEGER NOT NULL REFERENCES intervencija(id), 
    emso_prisotnega INTEGER NOT NULL REFERENCES clan(emso)
);

CREATE TABLE prisotnost_na_vajah (
    id SERIAL PRIMARY KEY, 
    id_vaje INTEGER NOT NULL REFERENCES vaja(id), 
    emso_prisotnega INTEGER NOT NULL REFERENCES clan(emso)
);

CREATE TABLE vozila_na_intervencijah (
    id SERIAL PRIMARY KEY, 
    id_intervencije INTEGER NOT NULL REFERENCES intervencija(id), 
    registracija_vozila TEXT NOT NULL REFERENCES vozilo(registrska_st)
);

CREATE TABLE ekipe_na_tekmovanjih (
    id SERIAL PRIMARY KEY, 
    id_tekmovanja INTEGER NOT NULL REFERENCES tekmovanje(id), 
    id_ekipe INTEGER NOT NULL REFERENCES ekipa(id),
    rezultat_opis TEXT NOT NULL
);

CREATE TABLE lastnistva_opreme (
    id SERIAL PRIMARY KEY,
    id_lastnika INTEGER REFERENCES clan(emso) DEFAULT 0,
    tip_opreme INTEGER NOT NULL REFERENCES osebna_oprema(id), 
    velikost TEXT,
    stevilo INTEGER
);

CREATE TABLE oprema_v_vozilih (
    id SERIAL PRIMARY KEY,
    registracija_vozila TEXT REFERENCES vozila(registrska_st) DEFAULT 0,
    tip_opreme INTEGER NOT NULL REFERENCES skupna_oprema(id), 
    dodatne_informacije TEXT
);

CREATE TABLE potrebuje_tecaj (
    id SERIAL PRIMARY KEY,
    id_opreme INTEGER NOT NULL REFERENCES skupna_oprema(id),
    id_tecaja INTEGER NOT NULL REFERENCES tecaj(id)
);

CREATE TABLE skrbnik_vozila (
    id SERIAL PRIMARY KEY, 
    emso_clana INTEGER NOT NULL REFERENCES clan(emso), 
    registracija_vozila TEXT NOT NULL REFERENCES vozilo(registrska_st)
);