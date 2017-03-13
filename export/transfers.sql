\echo 'asset_tag,request_by,request_dt,approve_by,approve_dt,source,destination,load_dt,unload_dt'

SELECT a.asset_tag, u.username FROM requests AS r INNER JOIN users AS u ON r.requester_fk=u.user_pk INNER JOIN assets AS a ON r.asset_fk=a.asset_pk;
