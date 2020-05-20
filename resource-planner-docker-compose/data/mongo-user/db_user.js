db = db.getSiblingDB('rp');

if (db.getUser('rpadmin') == null) {
    db.createUser({
        user: "rpadmin",
        pwd: "abcxyz123",
        roles: [{
            role: "readWrite",
            db: "rp"
        }]
    });
}