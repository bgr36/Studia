const express = require('express');
const router = express.Router();
const { User } = require('../models');
const db = require('../models');
const authenticateToken = require('../middleware/authMiddleware');
const authorizeRole = require('../middleware/roleMiddleware');

// GET /users - pobierz wszystkich użytkowników
router.get('/', async (req, res) => {
  try {
  const user = await db.User.findByPk(req.user.id, { attributes: ['id', 'username', 'email', 'role'] });
  res.json(user);
  } catch (err) {
    res.status(500).json({ error: 'Błąd przy pobieraniu użytkowników' });
  }
});

router.get('/me', authenticateToken, async (req, res) => {
  const user = await db.User.findByPk(req.user.id, { attributes: ['id', 'username', 'email', 'role'] });
  res.json(user);
});


// POST /users - utwórz nowego użytkownika
router.post('/', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    const newUser = await User.create({ username, email, password });
    res.status(201).json(newUser);
  } catch (err) {
    res.status(400).json({ error: 'Nie udało się utworzyć użytkownika' });
  }
});

// DELETE /users/:id - usuń użytkownika
router.delete('/:id', authenticateToken, authorizeRole('admin'), async (req, res) => {
  try {
    const deleted = await User.destroy({ where: { id: req.params.id } });
    if (!deleted) return res.status(404).json({ error: 'Nie znaleziono użytkownika' });
    res.json({ message: 'Użytkownik usunięty' });
  } catch (err) {
    res.status(500).json({ error: 'Błąd przy usuwaniu użytkownika' });
  }
});

module.exports = router;
