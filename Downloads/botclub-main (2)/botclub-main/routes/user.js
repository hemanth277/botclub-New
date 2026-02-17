const express = require("express");
const router = express.Router();
const User = require("../models/user");
const Product = require("../models/product");

// Get User Profile (Populated)
router.get("/profile", async (req, res) => {
    const { userId } = req.query;
    try {
        const user = await User.findById(userId)
            .populate('wishlist')
            .populate('cart.product');

        if (!user) return res.status(404).json({ message: "User not found" });

        // Sort cart to separate valid products from nulls (if product deleted)
        user.cart = user.cart.filter(item => item.product !== null);
        user.wishlist = user.wishlist.filter(item => item !== null);

        res.json(user);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Add to Wishlist
router.post("/wishlist", async (req, res) => {
    const { userId, productId } = req.body;
    try {
        const user = await User.findById(userId);
        if (!user.wishlist.includes(productId)) {
            user.wishlist.push(productId);
            await user.save();
        }
        res.json(user.wishlist);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Remove from Wishlist
router.delete("/wishlist", async (req, res) => {
    const { userId, productId } = req.body;
    try {
        const user = await User.findById(userId);
        user.wishlist = user.wishlist.filter(id => id.toString() !== productId);
        await user.save();
        res.json(user.wishlist);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Add to Cart
router.post("/cart", async (req, res) => {
    const { userId, productId } = req.body;
    try {
        const user = await User.findById(userId);
        const cartItem = user.cart.find(item => item.product.toString() === productId);

        if (cartItem) {
            cartItem.quantity += 1;
        } else {
            user.cart.push({ product: productId, quantity: 1 });
        }

        await user.save();
        // Populate to return full object
        await user.populate('cart.product');
        res.json(user.cart);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Update Cart Quantity
router.put("/cart", async (req, res) => {
    const { userId, productId, quantity } = req.body;
    try {
        const user = await User.findById(userId);
        const cartItem = user.cart.find(item => item.product.toString() === productId);

        if (cartItem) {
            cartItem.quantity = quantity;
            if (cartItem.quantity <= 0) {
                user.cart = user.cart.filter(item => item.product.toString() !== productId);
            }
        }

        await user.save();
        await user.populate('cart.product');
        // Filter out null products just in case
        user.cart = user.cart.filter(item => item.product !== null);
        res.json(user.cart);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Remove from Cart
router.delete("/cart", async (req, res) => {
    const { userId, productId } = req.body;
    try {
        const user = await User.findById(userId);
        user.cart = user.cart.filter(item => item.product.toString() !== productId);
        await user.save();
        res.json(user.cart);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;
