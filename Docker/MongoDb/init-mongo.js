db.auth('admin', 'mongo_admin_iot')

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