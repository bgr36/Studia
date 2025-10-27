const express = require('express');
const router = express.Router();
const { User } = require('../models');
const db = require('../models'); // Dołącz db, aby mieć dostęp do wszystkich modeli
const authenticateToken = require('../middleware/authMiddleware');
const authorizeRole = require('../middleware/roleMiddleware'); // Użyj authorizeRole z roleMiddleware.js

// Nowy endpoint: GET /users/all - pobierz wszystkich użytkowników (TYLKO DLA ADMINA)
router.get('/all', authenticateToken, authorizeRole('admin'), async (req, res) => {
  try {
    const users = await db.User.findAll({ attributes: ['id', 'username', 'email', 'role'] }); // Wybierz tylko potrzebne atrybuty
    res.json(users);
  } catch (err) {
    console.error('Błąd przy pobieraniu wszystkich użytkowników dla admina:', err);
    res.status(500).json({ error: 'Błąd serwera przy pobieraniu użytkowników', details: err.message });
  }
});

// Endpoint: GET /users/me - pobierz dane zalogowanego użytkownika (usuń istniejący GET /users i zastąp go tym)
// Zmieniam /users na /users/me, ponieważ /users powinien być uogólniony i to /users/all będzie odpytywane przez admina
router.get('/me', authenticateToken, async (req, res) => {
  try {
    const user = await db.User.findByPk(req.user.id, { attributes: ['id', 'username', 'email', 'role'] });
    if (!user) return res.status(404).json({ error: 'Użytkownik nie znaleziony' });
    res.json(user);
  } catch (err) {
    console.error('Błąd przy pobieraniu danych zalogowanego użytkownika:', err);
    res.status(500).json({ error: 'Błąd przy pobieraniu danych użytkownika', details: err.message });
  }
});


// POST /users - utwórz nowego użytkownika (dostępny dla wszystkich)
router.post('/', async (req, res) => {
  try {
    const { username, email, password, role } = req.body; // Dodaj 'role' do req.body
    // Sprawdź, czy rola jest dostarczona i czy jest prawidłowa, jeśli nie, ustaw domyślną
    const userRole = (role === 'admin' && req.user && req.user.role === 'admin') ? 'admin' : 'user';

    const newUser = await User.create({ username, email, password, role: userRole }); // Zapisz rolę
    res.status(201).json(newUser);
  } catch (err) {
    console.error("Błąd tworzenia użytkownika:", err.message);
    // Lepsze komunikaty błędów, np. z Sequelize ValidationErrors
    if (err.name === 'SequelizeUniqueConstraintError') {
      return res.status(409).json({ error: 'Użytkownik z takim loginem lub e-mailem już istnieje.' });
    }
    res.status(400).json({ error: 'Nie udało się utworzyć użytkownika', details: err.message });
  }
});

// PATCH /users/:id - edytuj użytkownika (tylko dla admina lub właściciela)
router.patch('/:id', authenticateToken, async (req, res) => {
  try {
    const { username, email, role } = req.body;
    const userIdToUpdate = parseInt(req.params.id);

    // Znajdź użytkownika do zaktualizowania
    const userToUpdate = await db.User.findByPk(userIdToUpdate);
    if (!userToUpdate) {
      return res.status(404).json({ error: 'Użytkownik nie znaleziony' });
    }

    // Sprawdź uprawnienia: tylko admin może edytować role lub innych użytkowników
    // Właściciel konta może edytować swoje dane (username, email), ale nie rolę.
    if (req.user.role !== 'admin' && req.user.id !== userIdToUpdate) {
      return res.status(403).json({ message: 'Brak uprawnień do edycji tego użytkownika.' });
    }

    // Admin może edytować wszystko (włącznie z rolą)
    if (req.user.role === 'admin') {
      await userToUpdate.update({ username, email, role });
    } else { // Zwykły użytkownik edytuje tylko swoje dane
      await userToUpdate.update({ username, email });
    }

    const updatedUser = await db.User.findByPk(userIdToUpdate, { attributes: ['id', 'username', 'email', 'role'] });
    res.status(200).json(updatedUser);
  } catch (err) {
    console.error("Błąd aktualizacji użytkownika:", err.message);
    if (err.name === 'SequelizeUniqueConstraintError') {
      return res.status(409).json({ error: 'Użytkownik z takim loginem lub e-mailem już istnieje.' });
    }
    res.status(500).json({ error: 'Błąd aktualizacji użytkownika', details: err.message });
  }
});


// DELETE /users/:id - usuń użytkownika (tylko dla admina)
router.delete('/:id', authenticateToken, authorizeRole('admin'), async (req, res) => {
  try {
    const deleted = await User.destroy({ where: { id: req.params.id } });
    if (!deleted) {
      return res.status(404).json({ error: 'Użytkownik nie znaleziony' });
    }
    res.status(204).send();
  } catch (err) {
    console.error("Błąd usuwania użytkownika:", err.message);
    res.status(500).json({ error: 'Błąd usuwania użytkownika', details: err.message });
  }
});

module.exports = router;