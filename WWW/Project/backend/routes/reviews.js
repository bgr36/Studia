const express = require('express');
const router = express.Router();
const db = require('../models'); // Zmień na db, aby mieć dostęp do wszystkich modeli
const Review = db.Review; // Pozostaw Review jako główny model
const authenticateToken = require('../middleware/authMiddleware');

// GET /reviews - pobierz wszystkie recenzje wraz z danymi użytkownika i produktu
router.get('/', async (req, res) => {
  try {
    const reviews = await Review.findAll({
      include: [
        {
          model: db.User, // Dołącz model User
          as: 'user',    // Użyj aliasu 'user' (zdefiniowanego w models/index.js)
          attributes: ['id', 'username'] // Wybierz tylko te atrybuty użytkownika
        },
        {
          model: db.Product, // Dołącz model Product
          as: 'product',   // Użyj aliasu 'product' (zdefiniowanego w models/index.js)
          attributes: ['id', 'name'] // Wybierz tylko te atrybuty produktu
        }
      ]
    });
    res.json(reviews);
  } catch (err) {
    console.error('Błąd przy pobieraniu recenzji:', err);
    res.status(500).json({ error: 'Błąd przy pobieraniu recenzji', details: err.message });
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
    console.error("Błąd tworzenia recenzji:", err.message);
    res.status(400).json({ error: 'Nie udało się stworzyć recenzji', details: err.message });
  }
});

// PATCH /reviews/:id
router.patch('/:id', async (req, res) => {
  try {
    const { comment } = req.body;
    const [updated] = await Review.update({ comment }, { where: { id: req.params.id } });
    if (!updated) return res.status(404).json({ error: 'Recenzja nie znaleziona' });
    const updatedReview = await Review.findByPk(req.params.id, {
        include: [
            { model: db.User, as: 'user', attributes: ['id', 'username'] },
            { model: db.Product, as: 'product', attributes: ['id', 'name'] }
        ]
    });
    res.status(200).json(updatedReview);
  } catch (err) {
    console.error("Błąd aktualizacji recenzji:", err.message);
    res.status(500).json({ error: 'Błąd aktualizacji recenzji', details: err.message });
  }
});

// DELETE /reviews/:id
router.delete('/:id', authenticateToken, async (req, res) => {
    try {
        // Dodatkowa logika: tylko właściciel recenzji lub admin może usunąć
        const review = await Review.findByPk(req.params.id);
        if (!review) {
            return res.status(404).json({ error: 'Recenzja nie znaleziona' });
        }
        // Sprawdź, czy użytkownik jest adminem lub jest właścicielem recenzji
        if (req.user.role !== 'admin' && review.userId !== req.user.id) {
            return res.status(403).json({ message: 'Brak uprawnień do usunięcia tej recenzji.' });
        }

        const deleted = await Review.destroy({ where: { id: req.params.id } });
        if (!deleted) {
            return res.status(404).json({ error: 'Recenzja nie znaleziona' });
        }
        res.status(204).send(); // 204 No Content for successful deletion
    } catch (err) {
        console.error("Błąd usuwania recenzji:", err.message);
        res.status(500).json({ error: 'Błąd usuwania recenzji', details: err.message });
    }
});


module.exports = router;