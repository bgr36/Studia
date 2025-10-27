const express = require('express');
const sequelize = require('./config/database');
const { User, Product, Review } = require('./models');
const userRoutes    = require('./routes/userRoutes');
const productRoutes = require('./routes/productRoutes');
const reviewRoutes  = require('./routes/reviewRoutes');
const errorHandler  = require('./middleware/errorHandler');

const app = express();
app.use(express.json());

// Synchronizacja modeli
sequelize.sync({ alter: true })
  .then(() => console.log('Baza danych zsynchronizowana'))
  .catch(err => console.error(err));

// Routes\ napp.use('/users', userRoutes);
app.use('/products', productRoutes);
app.use('/reviews', reviewRoutes);
app.use('/users', userRoutes);
app.use(errorHandler);

module.exports = app;