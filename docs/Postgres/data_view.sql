CREATE VIEW data_view AS 

 SELECT data_tbl.packet_rec_id, data_tbl.tag, data_tbl.subtag, data_tbl.seq, data_tbl.value 
   FROM data_tbl 
  ORDER BY data_tbl.packet_rec_id, data_tbl.tag, data_tbl.seq, data_tbl.subtag, data_tbl.value; 

