-- this is a trigger function for the transaction_tbl

CREATE OR REPLACE FUNCTION rpc_trigger_func()
  RETURNS trigger AS
'
DECLARE
	xgrant_number	text;
	xproject_id	text;
	xprid		int;
	xrecord		record;
BEGIN

RAISE DEBUG \'TG_NAME=% TG_OP=% TG_WHEN=% TG_RELNAME=%\', TG_NAME, TG_OP, TG_WHEN, TG_RELNAME;
-- find incoming rpc

	select into xprid p.packet_rec_id
	from   packet_tbl p, 
	       type_des   td
	where  p.trans_rec_id  = NEW.trans_rec_id
	and    p.outgoing_flag = 0
	and    p.type_id       = td.type_id
	and    td.type_name    = \'request_project_create\';

	if not found
	then
	    return NEW;
	end if;

RAISE DEBUG \'Found RPC=%\', xprid;

-- find completed outgoing npc

	select into xprid p.packet_rec_id
	from   packet_tbl p, 
	       type_des   td, 
	       state_des  sd
	where  p.trans_rec_id  = NEW.trans_rec_id
	and    p.outgoing_flag <> 0
	and    p.type_id       = td.type_id
	and    td.type_name    = \'notify_project_create\'
	and    p.state_id      = sd.state_id
	and    sd.state_name   = \'completed\';

	if not found
	then
	    return NEW;
	end if;

RAISE DEBUG \'Found NPC=%\', xprid;


-- get grant_number, project_id from the npc
	select into xgrant_number value
	from  data_tbl
	where packet_rec_id = xprid
	and   tag           = \'GrantNumber\';

	if not found
	then
	    raise EXCEPTION \'GrantNumber not present in NPC\';
	end if;
	
RAISE DEBUG \'GrantNumber=%\', xgrant_number;


	select into xproject_id value
	from  data_tbl
	where packet_rec_id = xprid
	and   tag           = \'ProjectID\';
	
RAISE DEBUG \'ProjectID=%\', xproject_id;

	if not exists (select * from project_tbl
		       where local_site_name  = NEW.local_site_name 
		       and   remote_site_name = NEW.remote_site_name 
		       and   grant_number     = xgrant_number
		       )
	then
RAISE DEBUG \'project_tbl(ls=%, rs=%, gn=%, pid=%)\', NEW.local_site_name, NEW.remote_site_name, xgrant_number, xproject_id;
	    insert into project_tbl (local_site_name, remote_site_name, grant_number, project_id)
	    values (NEW.local_site_name, NEW.remote_site_name, xgrant_number, xproject_id);
	end if;

-- find all the related RACs and release them

	for xrecord in 
	    select t.trans_rec_id
	    from   transaction_tbl t, 
	           packet_tbl      p,
	           data_tbl        d, 
	           type_des        td, 
	           state_des       sd
	    where  p.trans_rec_id  = t.trans_rec_id
	    and    t.state_id      = sd.state_id
	    and    sd.state_name   = \'on-hold\'
	    and    p.type_id       = td.type_id
	    and    td.type_name    = \'request_account_create\'
	    and    p.packet_rec_id = d.packet_rec_id
	    and    d.tag           = \'GrantNumber\'
	    and    d.value         = xgrant_number
	loop
RAISE DEBUG \'Found RAC in trans_rec_id=%\', xrecord.trans_rec_id;
	    update transaction_tbl
	    set    state_id = sd.state_id
	    from   state_des sd
	    where  trans_rec_id = xrecord.trans_rec_id
	    and    sd.state_name = \'in-progress\';

	end loop;
	    

	return NEW;
END;'
  LANGUAGE 'plpgsql' VOLATILE;
