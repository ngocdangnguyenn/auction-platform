create table packjetons
(
    id_pack       int auto_increment
        primary key,
    nombre_jetons int            not null,
    prix_pack     decimal(10, 2) not null
);

INSERT INTO web.packjetons (id_pack, nombre_jetons, prix_pack) VALUES (1, 10, 2.99);
INSERT INTO web.packjetons (id_pack, nombre_jetons, prix_pack) VALUES (2, 25, 5.99);
INSERT INTO web.packjetons (id_pack, nombre_jetons, prix_pack) VALUES (3, 50, 10.99);
INSERT INTO web.packjetons (id_pack, nombre_jetons, prix_pack) VALUES (4, 100, 19.99);
INSERT INTO web.packjetons (id_pack, nombre_jetons, prix_pack) VALUES (5, 500, 89.99);
