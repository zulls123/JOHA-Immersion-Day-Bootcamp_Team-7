const express = require('express');
const cors = require('cors');
const appRoutes = require('./routes/appRoutes');

const app = express();

app.use(cors());
app.set('view engine', 'ejs');
app.use('/', appRoutes);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});