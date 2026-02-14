const express = require("express");
const router = express.Router();
const Product = require("../models/product");

// Get all products
router.get("/", async (req, res) => {
  try {
    const products = await Product.find();
    res.json(products);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});


// Delete ALL products
router.delete("/", async (req, res) => {
  console.log("DELETE ALL request received");
  try {
    const result = await Product.deleteMany({});
    console.log(`Deleted ${result.deletedCount} products`);
    res.json({ message: `Deleted ${result.deletedCount} products` });
  } catch (err) {
    console.error("Error deleting all products:", err);
    res.status(500).json({ message: "Server Error: " + err.message });
  }
});

// Add a new product
router.post("/", async (req, res) => {
  const product = new Product({
    name: req.body.name,
    price: req.body.price,
    description: req.body.description,
    category: req.body.category,
    imageUrl: req.body.imageUrl,
    stock: req.body.stock,
  });

  try {
    const newProduct = await product.save();
    res.status(201).json(newProduct);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Update a product
router.put("/:id", async (req, res) => {
  console.log("PUT request received for ID:", req.params.id);
  console.log("Request Body:", req.body);
  try {
    const updatedProduct = await Product.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true, runValidators: true }
    );
    if (!updatedProduct) {
      console.log("Product not found with ID:", req.params.id);
      return res.status(404).json({ message: "Product not found" });
    }
    console.log("Product updated successfully:", updatedProduct);
    res.json(updatedProduct);
  } catch (err) {
    console.error("Error updating product:", err);
    res.status(500).json({ message: "Server Error: " + err.message });
  }
});

// Delete a product
router.delete("/:id", async (req, res) => {
  console.log("DELETE request received for ID:", req.params.id);
  try {
    const deletedProduct = await Product.findByIdAndDelete(req.params.id);
    if (!deletedProduct) {
      console.log("Product not found for deletion:", req.params.id);
      return res.status(404).json({ message: "Product not found" });
    }
    console.log("Product deleted:", req.params.id);
    res.json({ message: "Product deleted" });
  } catch (err) {
    console.error("Error deleting product:", err);
    res.status(500).json({ message: "Server Error: " + err.message });
  }
});

module.exports = router;
