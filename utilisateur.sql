create table utilisateur
(
    id_utilisateur  int auto_increment
        primary key,
    nom_utilisateur varchar(100)                not null,
    email           varchar(255)                not null,
    solde_jetons    decimal(10, 2) default 5.00 null,
    role            enum ('client', 'admin')    not null,
    constraint email
        unique (email)
);

INSERT INTO web.utilisateur (id_utilisateur, nom_utilisateur, email, solde_jetons, role) VALUES (1, 'John Doe', 'john.doe@example.com', null, 'client');
INSERT INTO web.utilisateur (id_utilisateur, nom_utilisateur, email, solde_jetons, role) VALUES (2, 'Alice Smith', 'alice.smith@example.com', null, 'client');
INSERT INTO web.utilisateur (id_utilisateur, nom_utilisateur, email, solde_jetons, role) VALUES (3, 'Bob Johnson', 'bob.johnson@example.com', null, 'client');
INSERT INTO web.utilisateur (id_utilisateur, nom_utilisateur, email, solde_jetons, role) VALUES (4, 'Admin User', 'admin@example.com', 1000.00, 'admin');
