const mongoose = require("mongoose");
const User = require("./models/user");
const bcrypt = require("bcryptjs");

mongoose.connect("mongodb://127.0.0.1:27017/ecommerce")
    .then(() => console.log("Connected to MongoDB"))
    .catch(err => console.error("Could not connect to MongoDB", err));

const updateAdmin = async () => {
    try {
        // 1. Remove old admin if exists
        const oldAdmin = await User.findOneAndDelete({ username: "admin" });
        if (oldAdmin) {
            console.log("Removed old 'admin' user.");
        } else {
            console.log("Old 'admin' user not found (or already removed).");
        }

        // 2. Remove 'botclub' if likely re-running script to ensure password update
        await User.findOneAndDelete({ username: "botclub" });

        // 3. Create new admin 'botclub'
        const hashedPassword = await bcrypt.hash("botclub1122", 10);
        const newAdmin = new User({
            username: "botclub",
            email: "botclub@rhinolifestyle.com", // Dummy email
            password: hashedPassword,
            role: "admin",
        });

        await newAdmin.save();
        console.log("New admin user 'botclub' created successfully!");
        console.log("Username: botclub");
        console.log("Password: botclub1122");

    } catch (err) {
        console.error("Error updating admin user:", err);
    } finally {
        mongoose.connection.close();
    }
};

updateAdmin();
