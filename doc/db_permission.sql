/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2020/7/11 8:48:09                            */
/*==============================================================*/


drop table if exists tab_menu;

drop table if exists tab_permission;

drop table if exists tab_permission_menu;

drop table if exists tab_role;

drop table if exists tab_role_permission;

drop table if exists tab_user;

drop table if exists tab_user_role;

/*==============================================================*/
/* Table: tab_menu                                              */
/*==============================================================*/
create table tab_menu
(
   id                   int not null auto_increment,
   name                 nvarchar(32),
   url                  nvarchar(32),
   parent_id            int,
   level                int,
   primary key (id)
);

/*==============================================================*/
/* Table: tab_permission                                        */
/*==============================================================*/
create table tab_permission
(
   id                   int not null auto_increment,
   name                 nvarchar(32),
   code                 nvarchar(32),
   primary key (id)
);

/*==============================================================*/
/* Table: tab_permission_menu                                   */
/*==============================================================*/
create table tab_permission_menu
(
   id                   int not null auto_increment,
   menu_id              int,
   permission_id        int,
   primary key (id)
);

/*==============================================================*/
/* Table: tab_role                                              */
/*==============================================================*/
create table tab_role
(
   id                   int not null auto_increment,
   name                 nvarchar(32),
   primary key (id)
);

/*==============================================================*/
/* Table: tab_role_permission                                   */
/*==============================================================*/
create table tab_role_permission
(
   id                   int not null auto_increment,
   role_id              int,
   permission_id        int,
   primary key (id)
);

/*==============================================================*/
/* Table: tab_user                                              */
/*==============================================================*/
create table tab_user
(
   id                   int not null auto_increment,
   loginName            nvarchar(32),
   password             nvarchar(32),
   name                 nvarchar(32),
   realName             nvarchar(32),
   mobile               nvarchar(11),
   address              nvarchar(255),
   email                nvarchar(32),
   lastLoginTime        date,
   status               int,
   primary key (id)
);

/*==============================================================*/
/* Table: tab_user_role                                         */
/*==============================================================*/
create table tab_user_role
(
   id                   int not null auto_increment,
   user_id              int,
   role_id              int,
   primary key (id)
);

alter table tab_permission_menu add constraint FK_Reference_4 foreign key (menu_id)
      references tab_menu (id) on delete restrict on update restrict;

alter table tab_permission_menu add constraint FK_Reference_7 foreign key (permission_id)
      references tab_permission (id) on delete restrict on update restrict;

alter table tab_role_permission add constraint FK_Reference_5 foreign key (role_id)
      references tab_role (id) on delete restrict on update restrict;

alter table tab_role_permission add constraint FK_Reference_6 foreign key (permission_id)
      references tab_permission (id) on delete restrict on update restrict;

alter table tab_user_role add constraint FK_Reference_1 foreign key (user_id)
      references tab_user (id) on delete restrict on update restrict;

alter table tab_user_role add constraint FK_Reference_2 foreign key (role_id)
      references tab_role (id) on delete restrict on update restrict;

