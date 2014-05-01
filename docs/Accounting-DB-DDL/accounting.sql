/*
 *  This is just used to create relations in local database for testing.
 *  The relations in the real database might be different.
 *
 */

CREATE TABLE public.user (
    username varchar(30) NOT NULL,
    unixid int NOT NULL,
    email varchar(100) NOT NULL,
    first_name varchar(100) NOT NULL,
    last_name varchar(100) NOT NULL,
    iu_user boolean,
    teragrid_user boolean,
    CONSTRAINT user_pk
      PRIMARY KEY  (username)
);

CREATE TABLE teragrid_project (
    id varchar(20) NOT NULL,
    status varchar(30) NOT NULL,
    CONSTRAINT project_id_pk
      PRIMARY KEY  (id)
);

CREATE TABLE teragrid_allocation (
    username varchar(30) NOT NULL,
    cluster_name varchar(30) NOT NULL,
    project varchar(20) NOT NULL,
    status varchar(30) NOT NULL
);

CREATE TABLE teragrid_resource_to_cluster (
    resource_name varchar(30) NOT NULL,
    cluster_name varchar(30) NOT NULL
);

CREATE TABLE cluster_account (
    username varchar(30) NOT NULL,
    cluster_name varchar(30) NOT NULL,
    status varchar(30) NOT NULL
);

CREATE TABLE cluster_account_group (
    username varchar(30) NOT NULL,
    cluster_name varchar(30) NOT NULL,
    group_name varchar(30) NOT NULL
);

CREATE TABLE cluster_account_primary_group (
    username varchar(30) NOT NULL,
    cluster_name varchar(30) NOT NULL,
    group_name varchar(30) NOT NULL
);

