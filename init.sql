/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2019/5/4 17:10:16                            */
/*==============================================================*/


drop table if exists `card effect state`;

drop table if exists `player cards`;

drop table if exists `players desk`;

drop table if exists `desk detail`;

drop table if exists `match`;

drop table if exists `player`;

drop table if exists `card`;

drop table if exists `desk`;

drop table if exists `effect`;




/*==============================================================*/
/* Table: card                                                  */
/*==============================================================*/
create table `card`
(
   `card name`          char(100),
   `cost`                 int,
   `class`                char(100),
   `rare`                 char(100),
   `card id`            int not null AUTO_INCREMENT,
   primary key (`card id`)
);

/*==============================================================*/
/* Table: "card effect state"                                   */
/*==============================================================*/
create table `card effect state`
(
   `card id`            int not null,
   `effect id`          int not null,
   primary key (`card id`, `effect id`)
);

/*==============================================================*/
/* Table: desk                                                  */
/*==============================================================*/
create table `desk`
(
   `class`              char(100),
   `desk id`            int not null AUTO_INCREMENT,
   `name`				char(100),
   primary key (`desk id`)
);

/*==============================================================*/
/* Table: "desk detail"                                         */
/*==============================================================*/
create table `desk detail`
(
   `card id`            int not null,
   `desk id`            int not null,
   primary key (`card id`, `desk id`)
);

/*==============================================================*/
/* Table: effect                                                */
/*==============================================================*/
create table `effect`
(
   `description`          char(100),
   `effect id`          int not null AUTO_INCREMENT,
   `effect type`        char(100),
   primary key (`effect id`)
);

/*==============================================================*/
/* Table: "match"                                               */
/*==============================================================*/
create table `match`
( 
   `round`              int,
   `match id`           int not null AUTO_INCREMENT,
   `winner id`          int not null,
   `loser id`           int not null,
   `loser desk id`      int not null,
   `winner desk id`     int not null,
   primary key (`match id`)
);

/*==============================================================*/
/* Table: player                                                */
/*==============================================================*/
create table player
(
   `money`              int,
   `dust`               int,
   `player id`          int not null AUTO_INCREMENT,
   `player name`        char(100),
   primary key (`player id`)
);

/*==============================================================*/
/* Table: "player cards"                                        */
/*==============================================================*/
create table `player cards`
(
   `card id`            int not null,
   `player id`          int not null,
   primary key (`card id`, `player id`)
);

/*==============================================================*/
/* Table: "players desk"                                        */
/*==============================================================*/
create table `players desk`
(
   `player id`          int not null,
   `desk id`            int not null,
   primary key (`player id`, `desk id`)
);

alter table `card effect state` add constraint `effect` foreign key (`effect id`)
      references effect (`effect id`) on delete restrict on update restrict;

alter table `card effect state` add constraint `effect card` foreign key (`card id`)
      references card (`card id`) on delete restrict on update restrict;

alter table `desk detail` add constraint `detail desk` foreign key (`desk id`)
      references desk (`desk id`) on delete restrict on update restrict;

alter table `desk detail` add constraint `desk card` foreign key (`card id`)
      references card (`card id`) on delete restrict on update restrict;

alter table `match` add constraint `loser` foreign key (`loser id`)
      references player (`player id`) on delete restrict on update restrict;

alter table `match` add constraint `loser_desk` foreign key (`loser desk id`)
      references desk (`desk id`) on delete restrict on update restrict;

alter table `match` add constraint `winner` foreign key (`winner id`)
      references player (`player id`) on delete restrict on update restrict;

alter table `match` add constraint `winner_desk` foreign key (`winner desk id`)
      references desk (`desk id`) on delete restrict on update restrict;

alter table `player cards` add constraint `FK_card2` foreign key (`player id`)
      references player (`player id`) on delete restrict on update restrict;

alter table `player cards` add constraint `FK_player2` foreign key (`card id`)
      references card (`card id`) on delete restrict on update restrict;

alter table `players desk` add constraint `player` foreign key (`player id`)
      references player (`player id`) on delete restrict on update restrict;

alter table `players desk` add constraint `player desk` foreign key (`desk id`)
      references desk (`desk id`) on delete restrict on update restrict;

