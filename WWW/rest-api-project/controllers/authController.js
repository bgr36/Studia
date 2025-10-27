const jwt = require('jsonwebtoken');
const db = require('../models');
const User = db.User;

exports.login = async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await User.findOne({ where: { email } });
    if (!user) return res.status(404).json({ error: 'Nie znaleziono użytkownika' });

    const isMatch = await user.validatePassword(password);
    if (!isMatch) return res.status(401).json({ error: 'Nieprawidłowe dane logowania' });

    const token = jwt.sign(
      { id: user.id, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );

    res.status(200).json({ message: 'Zalogowano pomyślnie', token });
  } catch (err) {
    res.status(500).json({ error: 'Błąd logowania', details: err.message });
  }
};
