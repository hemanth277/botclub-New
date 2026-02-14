const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const authRoutes = require("./routes/auth");
const productRoutes = require("./routes/product");
const userRoutes = require("./routes/user");

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static("public"));

mongoose.connect("mongodb://127.0.0.1:27017/ecommerce");

app.use("/api/auth", authRoutes);
app.use("/api/products", productRoutes);
app.use("/api/user", userRoutes);

app.listen(5000, () => {
  console.log("Server running on port 5000");
});
