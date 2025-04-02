create table enchere
(
    id_enchere    int auto_increment
        primary key,
    produit_id    int                                                       not null,
    date_debut    datetime                                                  not null,
    date_fin      datetime                                                  not null,
    jetons_requis decimal(10, 2)                                            not null,
    statut        enum ('ouverte', 'terminee', 'annulee') default 'ouverte' not null,
    gagnant_id    int                                                       null,
    constraint enchere_ibfk_1
        foreign key (produit_id) references produit (id_produit)
            on delete cascade,
    constraint enchere_ibfk_2
        foreign key (gagnant_id) references utilisateur (id_utilisateur)
            on delete set null
);

create index gagnant_id
    on enchere (gagnant_id);

create index produit_id
    on enchere (produit_id);

INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (1, 1, '2025-04-01 12:00:00', '2025-04-02 12:00:00', 5.00, 'ouverte', null);
INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (2, 2, '2025-04-02 15:00:00', '2025-04-03 15:00:00', 10.00, 'ouverte', null);
INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (3, 3, '2025-04-03 18:00:00', '2025-04-04 18:00:00', 7.00, 'ouverte', null);
INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (4, 4, '2025-04-04 20:00:00', '2025-04-05 20:00:00', 8.00, 'ouverte', null);
INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (5, 5, '2025-04-05 22:00:00', '2025-04-06 22:00:00', 6.00, 'ouverte', null);
INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (6, 1, '2025-04-01 12:00:00', '2025-04-02 12:00:00', 5.00, 'ouverte', null);
INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (7, 2, '2025-04-02 15:00:00', '2025-04-03 15:00:00', 10.00, 'ouverte', null);
INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (8, 3, '2025-04-03 18:00:00', '2025-04-04 18:00:00', 7.00, 'ouverte', null);
INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (9, 4, '2025-04-04 20:00:00', '2025-04-05 20:00:00', 8.00, 'ouverte', null);
INSERT INTO web.enchere (id_enchere, produit_id, date_debut, date_fin, jetons_requis, statut, gagnant_id) VALUES (10, 5, '2025-04-05 22:00:00', '2025-04-06 22:00:00', 6.00, 'ouverte', null);
