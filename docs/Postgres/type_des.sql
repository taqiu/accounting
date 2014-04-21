CREATE TABLE type_des 
(
    type_id   numeric(3,0) NOT NULL,
    type_name varchar(48)  NOT NULL,
    CONSTRAINT type_des_pk
      PRIMARY KEY (type_id),
    CONSTRAINT type_des_name_uk
      UNIQUE (type_name)
) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 1,'data_account_create' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 2,'data_project_create' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 3,'inform_transaction_complete' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 4,'notify_account_inactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 5,'notify_account_reactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 6,'notify_account_create' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 7,'notify_project_create' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 8,'notify_project_inactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 9,'notify_project_modify' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 10,'notify_project_reactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 11,'notify_project_resources' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 12,'notify_project_usage' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 13,'notify_user_modify' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 14,'notify_user_reactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 15,'notify_user_suspend' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 16,'request_account_create' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 17,'request_account_inactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 18,'request_account_reactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 19,'request_project_create' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 20,'request_project_inactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 21,'request_project_modify' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 22,'request_project_reactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 23,'request_project_resources' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 24,'request_user_modify' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 25,'request_user_reactivate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 26,'request_user_suspend' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 27,'request_user_create' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 28,'notify_user_create' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 29,'notify_person_ids' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 30,'notify_person_duplicate' ) ;

INSERT INTO type_des ( type_id, type_name ) VALUES ( 31,'request_person_merge' ) ;

