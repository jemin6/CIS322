\echo 'asset_tag,description,facility,acquired,disposed'

SELECT assets.asset_tag, assets.description, facilities.fcode, asset_at.arrive_dt, asset_at.disposed_dt FROM assets
INNER JOIN asset_at ON assets.asset_pk = asset_at.asset_fk
INNER JOIN facilities ON facilities.facility_pk=asset_at.facility_fk;
