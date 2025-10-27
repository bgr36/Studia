const express = require('express');
const app = express();
const db = require('./models');
require('dotenv').config();
const userRoutes = require('./routes/users');
const productRoutes = require('./routes/products');
const reviewRoutes = require('./routes/reviews');
const authRoutes = require('./routes/auth');
const cors = require('cors');

app.use(express.json());
app.use(cors());
app.use('/auth', authRoutes);
app.use(express.json());
app.use('/users', userRoutes);
app.use('/products', productRoutes);
app.use('/reviews', reviewRoutes);




// Synchronizacja bazy danych (na start w trybie force: true dla dev)
db.sequelize.sync({ force: true })
  .then(() => {
    console.log('Baza danych i tabele zostały utworzone');
  })
  .catch(err => console.log('Błąd synchronizacji bazy:', err));

// Testowy endpoint
app.get('/', (req, res) => {
  res.json({ message: 'REST API działa poprawnie' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Serwer działa na porcie ${PORT}`);
});