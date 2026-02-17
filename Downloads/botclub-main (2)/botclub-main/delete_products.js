const mongoose = require("mongoose");
const Product = require("./models/product");

mongoose.connect("mongodb://127.0.0.1:27017/ecommerce")
    .then(() => console.log("Connected to MongoDB for deletion"))
    .catch(err => console.error("Could not connect to MongoDB", err));

const deleteProducts = async () => {
    try {
        const result = await Product.deleteMany({});
        console.log(`Deleted ${result.deletedCount} products.`);
    } catch (err) {
        console.error("Error deleting products:", err);
    } finally {
        mongoose.connection.close();
    }
};

deleteProducts();
