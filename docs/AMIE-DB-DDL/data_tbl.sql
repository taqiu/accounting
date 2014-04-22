CREATE TABLE data_tbl 
(
    packet_rec_id  int           NOT NULL,
    tag            varchar(32)   NOT NULL,
    subtag         varchar(128)  NULL,
    seq            int           NOT NULL,
    value          text          NULL,
    CONSTRAINT data_uk
      UNIQUE  (packet_rec_id,tag,subtag,seq),
    CONSTRAINT data_packet_fk
      FOREIGN KEY (packet_rec_id)
      REFERENCES packet_tbl (packet_rec_id)
)
WITH OIDS;

CREATE INDEX data_prid_idx
  ON data_tbl
  USING btree
  (packet_rec_id);
  
CREATE INDEX data_prid_tag_idx
  ON data_tbl
  USING btree
  (packet_rec_id, tag);

