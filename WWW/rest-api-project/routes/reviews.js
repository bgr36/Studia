const express = require('express');
const router = express.Router();
const { Review } = require('../models');
const authenticateToken = require('../middleware/authMiddleware');


// GET /reviews
router.get('/', async (req, res) => {
  try {
    const reviews = await Review.findAll();
    res.json(reviews);
  } catch (err) {
    res.status(500).json({ error: 'Błąd przy pobieraniu recenzji' });
  }
});

// POST /reviews
router.post('/', authenticateToken, async (req, res) => {
  try {
    const { rating, comment, productId } = req.body;
    const userId = req.user.id; //z JWT

    const newReview = await Review.create({ rating, comment, productId, userId });
    res.status(201).json(newReview);
  } catch (err) {
    console.error("Błąd:", err.message);
    res.status(400).json({ error: 'Nie udało się stworzyć recenzji', details: err.message });
  }
});

// PATCH /reviews/:id
router.patch('/:id', async (req, res) => {
  try {
    const { comment } = req.body;
    const [updated] = await Review.update({ comment }, { where: { id: req.params.id } });
    if (!updated) return res.status(404).json({ error: 'Nie znaleziono recenzji' });
    const updatedReview = await Review.findByPk(req.params.id);
    res.json(updatedReview);
  } catch (err) {
    res.status(400).json({ error: 'Błąd przy aktualizacji recenzji' });
  }
});

module.exports = router;
