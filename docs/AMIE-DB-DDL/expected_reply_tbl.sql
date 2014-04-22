CREATE TABLE expected_reply_tbl 
(
    packet_rec_id int           NOT NULL,
    type_id       numeric(3,0)  NOT NULL,
    timeout       int           NULL,
    CONSTRAINT expected_reply_pk
      PRIMARY KEY (packet_rec_id,type_id),
    CONSTRAINT expected_reply_packet_fk
      FOREIGN KEY (packet_rec_id)
      REFERENCES packet_tbl (packet_rec_id),
    CONSTRAINT expected_reply_type_fk
      FOREIGN KEY (type_id)
      REFERENCES type_des (type_id)
) ;
