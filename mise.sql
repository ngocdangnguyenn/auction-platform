create table mise
(
    id_mise         int auto_increment
        primary key,
    id_utilisateur  int                                not null,
    id_enchere      int                                not null,
    montant_propose decimal(10, 2)                     not null,
    date_mise       datetime default CURRENT_TIMESTAMP not null,
    constraint unique_mise
        unique (id_enchere, montant_propose),
    constraint mise_ibfk_1
        foreign key (id_utilisateur) references utilisateur (id_utilisateur)
            on delete cascade,
    constraint mise_ibfk_2
        foreign key (id_enchere) references enchere (id_enchere)
            on delete cascade
);

create index id_utilisateur
    on mise (id_utilisateur);

INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (16, 1, 1, 5.99, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (17, 2, 1, 6.50, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (18, 3, 1, 5.20, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (19, 1, 2, 10.00, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (20, 2, 2, 9.50, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (21, 3, 2, 10.50, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (22, 1, 3, 7.30, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (23, 2, 3, 7.10, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (24, 1, 4, 8.20, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (25, 2, 4, 8.30, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (26, 3, 4, 8.25, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (27, 1, 5, 6.10, '2025-04-02 19:50:57');
INSERT INTO web.mise (id_mise, id_utilisateur, id_enchere, montant_propose, date_mise) VALUES (28, 2, 5, 6.50, '2025-04-02 19:50:57');
