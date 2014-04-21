CREATE VIEW packet_view AS 

 SELECT p.packet_rec_id, 
        p.packet_id, 
        td.type_name AS packet_type, 
        p."version", 
        sd1.state_name AS packet_state, 
        (p.outgoing_flag = 0::numeric ) AS is_incoming, 
        p.ts AS packet_ts,
        p.trans_rec_id,
        tr.originating_site_name, 
        tr.local_site_name, 
        tr.remote_site_name, 
        tr.transaction_id, 
        sd2.state_name AS transaction_state,
        tr.ts as transaction_ts
   FROM packet_tbl p, 
        type_des td, 
        state_des sd1, 
        transaction_tbl tr, 
        state_des sd2 
  WHERE p.state_id     = sd1.state_id
   AND  p.type_id      = td.type_id
   AND  p.trans_rec_id = tr.trans_rec_id
   AND  tr.state_id    = sd2.state_id; 

