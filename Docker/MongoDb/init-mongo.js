db.createUser(
    {
        user: 'admin',
        pwd: 'mongo_admin_iot',
        roles: [{ role: 'readWrite', db: 'iot_db' }]
    }
)
