const mongoose = require("mongoose");
const User = require("./models/user");

mongoose.connect("mongodb://127.0.0.1:27017/ecommerce")
    .then(() => console.log("Connected"))
    .catch(err => console.error("Error", err));

const checkAdmin = async () => {
    try {
        const admin = await User.findOne({ username: "admin" });
        console.log("Admin user found:", admin ? "YES" : "NO");
        if (admin) console.log("Role:", admin.role);
    } catch (e) {
        console.error(e);
    } finally {
        mongoose.connection.close();
    }
};
checkAdmin();
