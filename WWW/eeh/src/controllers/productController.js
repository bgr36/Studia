const { Product, User } = require('../models');
const { buildQuery } = require('../utils/query');

// Pobranie listy produktów z paginacją, filtrowaniem, sortowaniem
exports.list = async (req, res, next) => {
  try {
    const { filter, sort, pagination } = buildQuery(req.query);
    const products = await Product.findAll({
      where: filter,
      order: Object.entries(sort),
      offset: pagination.skip,
      limit: pagination.limit,
      include: [{ model: User, attributes: ['username'] }]
    });
    res.json(products);
  } catch (err) { next(err); }
};

// Pobranie produktu po ID
exports.get = async (req, res, next) => {
  try {
    const product = await Product.findByPk(req.params.id, {
      include: [{ model: User, attributes: ['username'] }]
    });
    if (!product) return res.status(404).json({ message: 'Nie znaleziono produktu' });
    res.json(product);
  } catch (err) { next(err); }
};

// Utworzenie produktu
exports.create = async (req, res, next) => {
  try {
    const prod = await Product.create({
      ...req.body,
      createdBy: req.user.id
    });
    res.status(201).json(prod);
  } catch (err) { next(err); }
};

// Aktualizacja produktu
exports.update = async (req, res, next) => {
  try {
    const [affectedRows, [updated]] = await Product.update(req.body, {
      where: { id: req.params.id },
      returning: true
    });
    if (!affectedRows) return res.status(404).json({ message: 'Nie znaleziono produktu' });
    res.json(updated);
  } catch (err) { next(err); }
};

// Usunięcie produktu
exports.remove = async (req, res, next) => {
  try {
    const count = await Product.destroy({ where: { id: req.params.id } });
    if (!count) return res.status(404).json({ message: 'Nie znaleziono produktu' });
    res.status(204).end();
  } catch (err) { next(err); }
};