const sequelize = require('../config/database');
const User = require('./user');
const Product = require('./product');
const Review = require('./review');

// Relacje
User.hasMany(Product, { foreignKey: 'createdBy' });
Product.belongsTo(User, { foreignKey: 'createdBy' });
Product.hasMany(Review, { foreignKey: 'productId' });
Review.belongsTo(Product, { foreignKey: 'productId' });
Review.belongsTo(User, { foreignKey: 'authorId' });
User.hasMany(Review, { foreignKey: 'authorId' });

module.exports = { sequelize, User, Product, Review };