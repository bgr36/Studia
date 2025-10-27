const express = require('express');
const router = express.Router();
const { Product } = require('../models');
const db = require('../models');
const { Op } = require('sequelize');
const authenticateToken = require('../middleware/authMiddleware');
const authorizeRole = require('../middleware/roleMiddleware');

// GET /products - pobierz wszystkie produkty
// router.get('/', async (req, res) => {
//   try {
//     const products = await Product.findAll();
//     res.json(products);
//   } catch (err) {
//     res.status(500).json({ error: 'Błąd przy pobieraniu produktów' });
//   }
// });

router.get('/', async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const offset = (page - 1) * limit;

    const minPrice = req.query.minPrice ? parseFloat(req.query.minPrice) : null;
    const maxPrice = req.query.maxPrice ? parseFloat(req.query.maxPrice) : null;

    let where = {};
    if (minPrice !== null || maxPrice !== null) {
      where.price = {};
      if (minPrice !== null) where.price[Op.gte] = minPrice;
      if (maxPrice !== null) where.price[Op.lte] = maxPrice;
    }

    let order = [['createdAt', 'DESC']];
    if (req.query.sort) {
      const [field, direction] = req.query.sort.split('_');
      order = [[field, direction.toUpperCase()]];
    }

    const products = await db.Product.findAndCountAll({
      where,
      order,
      limit,
      offset
    });

    res.json({
      totalItems: products.count,
      totalPages: Math.ceil(products.count / limit),
      currentPage: page,
      products: products.rows
    });
  } catch (error) {
    console.error('Błąd przy pobieraniu produktów:', error);
    res.status(500).json({ error: 'Błąd serwera' });
  }
});

// POST /products
router.post('/', authenticateToken, authorizeRole('admin'), async (req, res) => {
  try {
    const { name, description, price } = req.body;
    const newProduct = await Product.create({ name, description, price });
    res.status(201).json(newProduct);
  } catch (err) {
    res.status(400).json({ error: 'Nie udało się utworzyć produktu' });
  }
});

// PUT /products/:id
router.put('/:id', authenticateToken, authorizeRole('admin'), async (req, res) => {
  try {
    const { name, description, price } = req.body;
    const [updated] = await Product.update({ name, description, price }, { where: { id: req.params.id } });
    if (!updated) return res.status(404).json({ error: 'Produkt nie istnieje' });
    const updatedProduct = await Product.findByPk(req.params.id);
    res.json(updatedProduct);
  } catch (err) {
    res.status(400).json({ error: 'Błąd przy aktualizacji produktu' });
  }
});

module.exports = router;