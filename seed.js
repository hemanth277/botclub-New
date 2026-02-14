const mongoose = require("mongoose");
const Product = require("./models/product");

mongoose.connect("mongodb://127.0.0.1:27017/ecommerce")
    .then(() => console.log("Connected to MongoDB for seeding"))
    .catch(err => console.error("Could not connect to MongoDB", err));

const categories = ["Men", "Women", "Kids"];
const productTypes = ["T-Shirt", "Jeans", "Jacket", "Shoes", "Hat", "Watch", "Bag", "Dress", "Skirt", "Shorts"];
const adjectives = ["Premium", "Classic", "Modern", "Urban", "Vintage", "Sport", "Elegant", "Casual", "Luxury", "Essential"];

const products = [];

for (let i = 0; i < 100; i++) {
    const category = categories[Math.floor(Math.random() * categories.length)];
    const type = productTypes[Math.floor(Math.random() * productTypes.length)];
    const adj = adjectives[Math.floor(Math.random() * adjectives.length)];

    products.push({
        name: `${adj} ${category} ${type}`,
        price: parseFloat((Math.random() * 100 + 20).toFixed(2)),
        description: `A high-quality ${type.toLowerCase()} for ${category.toLowerCase()}. Perfect for any occasion.`,
        category: category,
        imageUrl: `https://source.unsplash.com/random/300x300/?fashion,${category},${type}`,
        stock: Math.floor(Math.random() * 100) + 1
    });
}

const seedDB = async () => {
    try {
        await Product.deleteMany({});
        console.log("Cleared existing products");
        await Product.insertMany(products);
        console.log("Added 100 new products!");
    } catch (err) {
        console.error("Error seeding database:", err);
    } finally {
        mongoose.connection.close();
    }
};

seedDB();
