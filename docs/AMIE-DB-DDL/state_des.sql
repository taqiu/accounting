CREATE TABLE state_des 
(
    state_id   numeric(3,0) NOT NULL,
    state_name varchar(32)  NOT NULL,
    CONSTRAINT state_des_pk
      PRIMARY KEY (state_id),
    CONSTRAINT state_des_name_uk
      UNIQUE (state_name)
) ;

INSERT INTO state_des ( state_id, state_name ) VALUES ( 1,'completed' ) ;

INSERT INTO state_des ( state_id, state_name ) VALUES ( 2,'in-progress' ) ;

INSERT INTO state_des ( state_id, state_name ) VALUES ( 3,'failed' ) ;

INSERT INTO state_des ( state_id, state_name ) VALUES ( 4,'rejected' ) ;

INSERT INTO state_des ( state_id, state_name ) VALUES ( 5,'on-hold' ) ;

INSERT INTO state_des ( state_id, state_name ) VALUES ( 6,'x-pending' ) ;

INSERT INTO state_des ( state_id, state_name ) VALUES ( 7,'killed' ) ;
