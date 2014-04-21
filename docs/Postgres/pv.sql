CREATE VIEW pv AS 

 SELECT t.trans_rec_id as trid,
        p.packet_rec_id as prid, 
        t.transaction_id as tid, 
        p.packet_id as pid, 
        td.type_name AS ptype, 
        ps.state_name AS pstate, 
        (p.outgoing_flag = 0::numeric) AS incoming, 
        p.ts AS ptime,
        t.originating_site_name as os, 
        t.local_site_name as ls, 
        t.remote_site_name as rs, 
        ts.state_name AS tstate,
        t.ts as ttime
   FROM packet_tbl p, 
        type_des td, 
        state_des ps, 
        transaction_tbl t, 
        state_des ts 
  WHERE p.trans_rec_id = t.trans_rec_id
    AND p.state_id     = ps.state_id
    AND p.type_id      = td.type_id
    AND t.state_id     = ts.state_id

   ORDER BY 1,2
;
