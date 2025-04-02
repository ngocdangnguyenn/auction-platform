create table achatjetons
(
    id_achat       int auto_increment
        primary key,
    id_utilisateur int                                not null,
    id_pack        int                                not null,
    date_achat     datetime default CURRENT_TIMESTAMP not null,
    constraint achatjetons_ibfk_1
        foreign key (id_utilisateur) references utilisateur (id_utilisateur)
            on delete cascade,
    constraint achatjetons_ibfk_2
        foreign key (id_pack) references packjetons (id_pack)
            on delete cascade
);

create index id_pack
    on achatjetons (id_pack);

create index id_utilisateur
    on achatjetons (id_utilisateur);

INSERT INTO web.achatjetons (id_achat, id_utilisateur, id_pack, date_achat) VALUES (1, 1, 2, '2025-04-01 14:00:00');
INSERT INTO web.achatjetons (id_achat, id_utilisateur, id_pack, date_achat) VALUES (2, 2, 3, '2025-04-02 10:00:00');
INSERT INTO web.achatjetons (id_achat, id_utilisateur, id_pack, date_achat) VALUES (3, 3, 1, '2025-04-03 16:30:00');
INSERT INTO web.achatjetons (id_achat, id_utilisateur, id_pack, date_achat) VALUES (4, 1, 5, '2025-04-04 09:45:00');
INSERT INTO web.achatjetons (id_achat, id_utilisateur, id_pack, date_achat) VALUES (5, 2, 4, '2025-04-05 11:15:00');
