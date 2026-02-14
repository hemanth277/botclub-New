const express = require("express");
const router = express.Router();
const User = require("../models/user");
const bcrypt = require("bcryptjs");

// Register
router.post("/register", async (req, res) => {
  try {
    const hashedPassword = await bcrypt.hash(req.body.password, 10);
    const user = new User({
      username: req.body.username,
      email: req.body.email,
      password: hashedPassword,
      role: req.body.role || "customer",
    });
    const newUser = await user.save();
    res.status(201).json(newUser);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Login
router.post("/login", async (req, res) => {
  try {
    const user = await User.findOne({ username: req.body.username });
    if (!user) return res.status(400).json({ message: "User not found" });

    const isValid = await bcrypt.compare(req.body.password, user.password);
    if (!isValid) return res.status(400).json({ message: "Invalid password" });

    res.json({ message: "Login successful", user: { id: user._id, username: user.username, role: user.role } });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;
