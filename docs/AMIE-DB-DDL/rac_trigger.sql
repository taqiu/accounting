CREATE TRIGGER rac_trigger
  AFTER UPDATE
  ON packet_tbl
  FOR EACH ROW
  EXECUTE PROCEDURE rac_trigger_func();
