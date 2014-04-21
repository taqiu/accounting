CREATE TABLE transaction_depends_tbl 
(
    trans_rec_id            int NOT NULL,
    depends_on_trans_rec_id int NOT NULL,
    CONSTRAINT transaction_depends_uk
      UNIQUE  (trans_rec_id,depends_on_trans_rec_id),
    CONSTRAINT transaction_depends_fk1
      FOREIGN KEY (trans_rec_id)
      REFERENCES transaction_tbl (trans_rec_id),
    CONSTRAINT transaction_depends_fk2
      FOREIGN KEY (depends_on_trans_rec_id)
      REFERENCES transaction_tbl (trans_rec_id)
) ;
