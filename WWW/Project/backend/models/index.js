const { Sequelize } = require('sequelize');
require('dotenv').config();

const sequelize = new Sequelize(process.env.DB_NAME, process.env.DB_USER, process.env.DB_PASS, {
  host: process.env.DB_HOST,
  dialect: 'mariadb',
  port: process.env.DB_PORT,
  logging: false,
});

const db = {};

db.Sequelize = Sequelize;
db.sequelize = sequelize;

db.User = require('./user')(sequelize, Sequelize);
db.Product = require('./product')(sequelize, Sequelize);
db.Review = require('./review')(sequelize, Sequelize);

// Relacje
db.User.hasMany(db.Review, { foreignKey: 'userId', as: 'reviews' });
db.Review.belongsTo(db.User, { foreignKey: 'userId', as: 'user' });

db.Product.hasMany(db.Review, { foreignKey: 'productId', as: 'reviews' });
db.Review.belongsTo(db.Product, { foreignKey: 'productId', as: 'product' });

module.exports = db;
