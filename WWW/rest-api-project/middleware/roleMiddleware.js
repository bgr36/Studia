function authorizeRole(role) {
  return (req, res, next) => {
    if (!req.user || req.user.role !== role) {
      return res.status(403).json({ error: 'Brak uprawnień' });
    }
    next();
  };
}

module.exports = authorizeRole;