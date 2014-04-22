CREATE TABLE packet_tbl 
(
    packet_rec_id serial,
    trans_rec_id  int           NOT NULL,
    packet_id     numeric(38,0) NOT NULL,
    type_id       numeric(3,0)  NOT NULL,
    version       varchar(4)    NOT NULL,
    state_id      numeric(3,0)  NOT NULL,
    outgoing_flag numeric(1,0)  NOT NULL,
    ts            timestamp     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT packet_pk
      PRIMARY KEY  (packet_rec_id),
    CONSTRAINT packet_uk
      UNIQUE  (trans_rec_id,packet_id,outgoing_flag),
    CONSTRAINT packet_type_fk
      FOREIGN KEY (type_id)
      REFERENCES type_des (type_id),
    CONSTRAINT packet_state_fk
      FOREIGN KEY (state_id)
      REFERENCES state_des (state_id),
    CONSTRAINT packet_trans_fk
      FOREIGN KEY (trans_rec_id)
      REFERENCES transaction_tbl (trans_rec_id)
) ;

