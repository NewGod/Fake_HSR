/*==============================================================*/
/* DBMS name:      MySQL 8.0                                    */
/* Created on:     2019/5/12 15:32:38                           */
/*==============================================================*/

drop view if exists `card effect view`;

drop view if exists `player desk view`;

drop view if exists `desk view`;

drop table if exists `card effect state`;

drop table if exists `desk detail`;

drop table if exists `player card`;

drop table if exists `player desk`;

drop table if exists `match`;

drop table if exists `card`;

drop table if exists `desk`;

drop table if exists `effect`;

drop table if exists `player`;

/*==============================================================*/
/* Table: `card effect state`                                   */
/*==============================================================*/
create table `card effect state`
(
   `card id`            int not null,
   `effect id`          int not null,
   primary key (`card id`, `effect id`)
);

/*==============================================================*/
/* Table: card                                                 */
/*==============================================================*/
create table `card`
(
   `card name`          char(100),
   `cost`                 int,
   `class`                char(100),
   `rare`                 char(100),
   `card id`            int not null AUTO_INCREMENT,
   primary key (`card id`),
   index (`cost`, `card name`),
   index (`card name`)
);

/*==============================================================*/
/* Table: `desk detail`                                         */
/*==============================================================*/
create table `desk detail`
(
   `card id`            int not null,
   `desk id`            int not null,
   `card detail id`     int not null AUTO_INCREMENT,
   primary key (`card detail id`)
);

/*==============================================================*/
/* Table: desk                                                 */
/*==============================================================*/
create table `desk`
(
   `class`                char(100),
   `desk id`            int not null auto_increment,
   `build type`         char(100),
   primary key (`desk id`),
   index (`build type`)
);

/*==============================================================*/
/* Table: effect                                               */
/*==============================================================*/
create table `effect`
(
   `description`          char(100),
   `effect id`          int not null auto_increment,
   `effect type`        char(100),
   primary key (`effect id`),
   index (`effect type`, `description`)
);

/*==============================================================*/
/* Table: `match`                                               */
/*==============================================================*/
create table `match`
(
   `round`                int,
   `process`              blob,
   `match id`           int not null auto_increment,
   `winner id`          int not null,
   `loser id`           int not null,
   `loser desk id`      int not null,
   `winner desk id`     int not null,
   primary key (`match id`)
);

/*==============================================================*/
/* Table: `player card`                                        */
/*==============================================================*/
create table `player card`
(
   `card id`            int not null,
   `player id`          int not null,
   `player card id`    int not null auto_increment,
   primary key (`player card id`)
);

/*==============================================================*/
/* Table: player                                               */
/*==============================================================*/
create table player
(
   money                int,
   dust                 int,
   `player id`          int not null auto_increment,
   `player name`        char(100),
   primary key (`player id`)
);

/*==============================================================*/
/* Table: `player desk`                                        */
/*==============================================================*/
create table `player desk`
(
   `player id`          int not null,
   `desk id`            int not null,
   `player desk id`    int not null auto_increment,
   primary key (`player desk id`)
);

alter table `card effect state` add constraint FK_effot foreign key (`effect id`)
      references effect (`effect id`) on delete restrict on update restrict;

alter table `card effect state` add constraint FK_card foreign key (`card id`)
      references card (`card id`) on delete restrict on update restrict;

alter table `desk detail` add constraint FK_desk foreign key (`desk id`)
      references desk (`desk id`) on delete restrict on update restrict;

alter table `desk detail` add constraint FK_card2 foreign key (`card id`)
      references card (`card id`) on delete restrict on update restrict;

alter table `match` add constraint FK_loser foreign key (`loser id`)
      references player (`player id`) on delete restrict on update restrict;

alter table `match` add constraint FK_loser_desk foreign key (`loser desk id`)
      references desk (`desk id`) on delete restrict on update restrict;

alter table `match` add constraint FK_winner foreign key (`winner id`)
      references player (`player id`) on delete restrict on update restrict;

alter table `match` add constraint FK_winner_desk foreign key (`winner desk id`)
      references desk (`desk id`) on delete restrict on update restrict;

alter table `player card` add constraint FK_card3 foreign key (`player id`)
      references player (`player id`) on delete restrict on update restrict;

alter table `player card` add constraint FK_player1 foreign key (`card id`)
      references card (`card id`) on delete restrict on update restrict;

alter table `player desk` add constraint FK_player2 foreign key (`player id`)
      references player (`player id`) on delete restrict on update restrict;

alter table `player desk` add constraint FK_desk2 foreign key (`desk id`)
      references desk (`desk id`) on delete restrict on update restrict;

create view `card effect view` as 
	select 
		b.`card id` `card id`, 
		c.`effect id` `effect id`, 
		c.`effect type` `effect type` 
	from `card effect state` b join `effect` c on 
		b.`effect id` = c.`effect id`;

create view `desk view` as 
	select 
		a.`desk id` `id`, 
		a.`class` `class`, 
		a.`build type` `name`, 
		count(b.`match id`) `match times`, 
		count(if(b.`winner desk id` = a.`desk id`, 1, NULL)) `win`,
		count(if(b.`loser desk id` = a.`desk id`, 1, NULL)) `lose`, 
		avg(b.`round`) `average round` 
	from `desk` a left join `match` b on 
		a.`desk id` = b.`winner desk id` 
		or a.`desk id` = b.`loser desk id` 
	group by a.`desk id`;

create view `player desk view` as 
    select a.`player id` `player id`, b.`desk id` `desk id`, b.`build type` `name` 
	from `player desk` a join `desk` b 
		on a.`desk id`=b.`desk id`;
