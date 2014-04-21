-- this is a trigger function for the packet_tbl

CREATE OR REPLACE FUNCTION rac_trigger_func()
  RETURNS trigger AS
'
DECLARE
	xgrant_number	text;
	xrac		int;
	xon_hold	int;
	xin_progress	int;
BEGIN

RAISE DEBUG \'TG_NAME=% TG_OP=% TG_WHEN=% TG_RELNAME=%\', TG_NAME, TG_OP, TG_WHEN, TG_RELNAME;
	select into xrac type_id from type_des where type_name = \'request_account_create\';
	select into xon_hold state_id from state_des where state_name = \'on-hold\';
	select into xin_progress state_id from state_des where state_name = \'in-progress\';

-- is this an incoming rac?

	if NEW.type_id <> xrac
	or NEW.outgoing_flag <> 0
	then
	    return NEW;
	end if;

-- going from on-hold to in-progress?
	if OLD.state_id <> xon_hold
	or NEW.state_id <> xin_progress
	then
		return NEW;
	end if;


RAISE DEBUG \'Incoming RAC(%)\', NEW.packet_rec_id;

	select into xgrant_number value
	from  data_tbl
	where packet_rec_id = NEW.packet_rec_id
	and   tag           = \'GrantNumber\';

	if not found
	then
	    raise EXCEPTION \'GrantNumber not present in RAC\';
	end if;

RAISE DEBUG \'GrantNumber=%\', xgrant_number;
	
	if not exists (select * from project_tbl p, transaction_tbl t
		       where t.trans_rec_id     = NEW.trans_rec_id
		       and   t.local_site_name  = t.local_site_name 
		       and   t.remote_site_name = t.remote_site_name 
		       and   p.grant_number     = xgrant_number
		       )
	then
RAISE DEBUG \'Project not yet created, put RAC on-hold\';
	    update transaction_tbl
	    set state_id = xon_hold
	    where trans_rec_id = NEW.trans_rec_id;
	end if;

	return NEW;
END;'
  LANGUAGE 'plpgsql' VOLATILE;
