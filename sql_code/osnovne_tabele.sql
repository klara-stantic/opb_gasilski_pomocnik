CREATE TABLE funkcija (
    id_funkcija SERIAL PRIMARY KEY, 
    naziv TEXT NOT NULL
);

CREATE TABLE cin (
    id_cin SERIAL PRIMARY KEY, 
    cin TEXT NOT NULL
);

CREATE TABLE clan (
    emso INTEGER PRIMARY KEY,
    ime TEXT NOT NULL, 
    priimek TEXT NOT NULL,
    funkcija INTEGER NOT NULL REFERENCES funkcija(id_funkcija), 
    cin INTEGER NOT NULL REFERENCES cin(id_cin),
    zdravniski DATE, 
    aktiven BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE tip_vozila (
    id_vozilo SERIAL PRIMARY KEY, 
    tip_vozila TEXT NOT NULL, 
    opis_tipa TEXT NOT NULL
);

CREATE TABLE kategorija_vozniskega_dovoljenja (
    id_kategorije SERIAL PRIMARY KEY,
    kategorija TEXT NOT NULL
);

CREATE TABLE vozilo (
    registrska_st TEXT NOT NULL PRIMARY KEY,
    tip_vozila INTEGER NOT NULL REFERENCES tip_vozila(id_vozilo),
    potreben_izpit INTEGER NOT NULL REFERENCES kategorija_vozniskega_dovoljenja(id_kategorije),
    st_potnikov INTEGER NOT NULL,
    znamka TEXT NOT NULL,
    tehnicni DATE,
    aktivno BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE tip_intervencije (
    id_tipa_intervencije SERIAL PRIMARY KEY, 
    tip TEXT NOT NULL
);

CREATE TABLE intervencija (
    id SERIAL PRIMARY KEY,
    opis TEXT,
    datum DATE NOT NULL,
    tip INTEGER NOT NULL REFERENCES tip_intervencije(id_tipa_intervencije)
);

CREATE TABLE osebna_oprema (
    id SERIAL PRIMARY KEY,
    tip_opreme TEXT NOT NULL
);

CREATE TABLE skupna_oprema (
    id SERIAL PRIMARY KEY,
    tip_opreme TEXT NOT NULL
);

CREATE TABLE tip_tecaja (
    id_tecaj SERIAL PRIMARY KEY, 
    naziv_tecaja TEXT NOT NULL 
);

CREATE TABLE tecaj (
    id SERIAL PRIMARY KEY,
    naziv_tecaja INTEGER NOT NULL REFERENCES tip_tecaja(id_tecaj),
    datum DATE NOT NULL, 
    organizator TEXT NOT NULL, 
    cena FLOAT
);

CREATE TABLE vaja (
    id SERIAL PRIMARY KEY,
    datum DATE NOT NULL, 
    obvezna BOOLEAN NOT NULL, 
    tip_vaje INTEGER NOT NULL REFERENCES tip_intervencije(id_tipa_intervencije), 
    vodja INTEGER REFERENCES clan(emso)
);

CREATE TABLE tip_tekmovanja (
    id_tip SERIAL PRIMARY KEY, 
    tip TEXT NOT NULL
);

CREATE TABLE tekmovanje (
    id SERIAL PRIMARY key,  
    lokacija TEXT NOT NULL, 
    tip_tekmovanja INTEGER NOT NULL REFERENCES tip_tekmovanja(id_tip),
    datum DATE NOT NULL
);

CREATE TABLE ekipa (
    id SERIAL PRIMARY KEY
);
