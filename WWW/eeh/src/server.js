const app = require('./app');
const { PORT } = process.env;

app.listen(PORT, () => console.log(`Server działa na porcie ${PORT}`))