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