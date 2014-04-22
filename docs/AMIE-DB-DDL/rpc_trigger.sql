CREATE TRIGGER rpc_trigger
  AFTER UPDATE
  ON transaction_tbl
  FOR EACH ROW
  EXECUTE PROCEDURE rpc_trigger_func();
