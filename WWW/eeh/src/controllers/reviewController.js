const { Review, Product, User } = require('../models');

// Lista recenzji, opcjonalnie filtrowana po productId
exports.list = async (req, res, next) => {
  try {
    const where = {};
    if (req.query.productId) where.productId = req.query.productId;
    const reviews = await Review.findAll({
      where,
      include: [
        { model: User, as: 'User', attributes: ['username'] },
        { model: Product, attributes: ['name'] }
      ]
    });
    res.json(reviews);
  } catch (err) { next(err); }
};

// Pobranie recenzji po ID
exports.get = async (req, res, next) => {
  try {
    const review = await Review.findByPk(req.params.id, {
      include: [ { model: User, attributes: ['username'] }, { model: Product, attributes: ['name'] } ]
    });
    if (!review) return res.status(404).json({ message: 'Nie znaleziono recenzji' });
    res.json(review);
  } catch (err) { next(err); }
};

// Utworzenie recenzji
exports.create = async (req, res, next) => {
  try {
    const rev = await Review.create({
      ...req.body,
      authorId: req.user.id
    });
    res.status(201).json(rev);
  } catch (err) { next(err); }
};

// Aktualizacja recenzji
exports.update = async (req, res, next) => {
  try {
    const [count, [updated]] = await Review.update(req.body, {
      where: { id: req.params.id },
      returning: true
    });
    if (!count) return res.status(404).json({ message: 'Nie znaleziono recenzji' });
    res.json(updated);
  } catch (err) { next(err); }
};

// Usunięcie recenzji
exports.remove = async (req, res, next) => {
  try {
    const count = await Review.destroy({ where: { id: req.params.id } });
    if (!count) return res.status(404).json({ message: 'Nie znaleziono recenzji' });
    res.status(204).end();
  } catch (err) { next(err); }
};