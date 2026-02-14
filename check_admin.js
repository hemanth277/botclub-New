require("dotenv").config();
const mongoose = require("mongoose");
const User = require("./models/user");

const MONGO_URI = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/ecommerce";

mongoose.connect(MONGO_URI)
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
