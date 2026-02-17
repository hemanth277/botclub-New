require("dotenv").config();
const mongoose = require("mongoose");
const User = require("./models/user");
const bcrypt = require("bcryptjs");

const MONGO_URI = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/ecommerce";

mongoose.connect(MONGO_URI)
    .then(() => console.log("Connected to MongoDB"))
    .catch(err => console.error("Could not connect to MongoDB", err));

const createAdmin = async () => {
    try {
        // Check if admin already exists
        const existingAdmin = await User.findOne({ username: "admin" });
        if (existingAdmin) {
            console.log("Admin user already exists!");
            return;
        }

        const hashedPassword = await bcrypt.hash("admin123", 10);
        const adminUser = new User({
            username: "admin",
            email: "admin@rhinolifestyle.com",
            password: hashedPassword,
            role: "admin",
        });

        await adminUser.save();
        console.log("Admin user created successfully!");
        console.log("Username: admin");
        console.log("Password: admin123");
    } catch (err) {
        console.error("Error creating admin user:", err);
    } finally {
        mongoose.connection.close();
    }
};

createAdmin();
