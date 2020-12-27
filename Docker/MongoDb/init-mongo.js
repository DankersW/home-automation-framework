//db.auth('admin', 'mongo_admin_iot')

/*
db.createUser(
    {
        user: "admin",
        pwd: "mongo_admin_iot",
        roles: [
            "userAdminAnyDatabase",
            "dbAdminAnyDatabase",
            "readWriteAnyDatabase"
        ]
    }
)
*/


db = db.getSiblingDB('iot_db');
db.createUser(
    {
        user: 'admin',
        pwd: 'mongo_admin_iot',
        roles: [{ role: 'readWrite', db: 'api_prod_db' }],
    },
);