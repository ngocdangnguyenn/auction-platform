create table produit
(
    id_produit   int auto_increment
        primary key,
    nom_produit  varchar(100)   not null,
    description  text           null,
    prix_produit decimal(10, 2) not null
);

INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (1, 'iPhone 15', 'Smartphone dernière génération', 999.99);
INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (2, 'MacBook Pro', 'Ordinateur portable Apple', 1899.99);
INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (3, 'PlayStation 5', 'Console de jeu Sony', 499.99);
INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (4, 'Samsung Galaxy S24', 'Smartphone Android puissant', 899.99);
INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (5, 'TV OLED 55"', 'Téléviseur OLED 4K', 1499.99);
INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (6, 'iPhone 15', 'Smartphone dernière génération', 999.99);
INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (7, 'MacBook Pro', 'Ordinateur portable Apple', 1899.99);
INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (8, 'PlayStation 5', 'Console de jeu Sony', 499.99);
INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (9, 'Samsung Galaxy S24', 'Smartphone Android puissant', 899.99);
INSERT INTO web.produit (id_produit, nom_produit, description, prix_produit) VALUES (10, 'TV OLED 55"', 'Téléviseur OLED 4K', 1499.99);
