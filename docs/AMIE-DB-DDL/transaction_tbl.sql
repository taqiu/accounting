CREATE TABLE transaction_tbl 
(
    trans_rec_id          serial,
    originating_site_name varchar(16)   NOT NULL,
    transaction_id        numeric(38,0) NOT NULL,
    local_site_name       varchar(16)   NOT NULL,
    remote_site_name      varchar(16)   NOT NULL,
    state_id              numeric(3,0)  NOT NULL,
    ts                    timestamp     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT transaction_pk
      PRIMARY KEY  (trans_rec_id),
    CONSTRAINT transaction_uk
      UNIQUE  (originating_site_name,transaction_id,local_site_name,remote_site_name),
    CONSTRAINT transaction_state_fk
      FOREIGN KEY (state_id)
      REFERENCES state_des (state_id)
) ;
