const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/user');

const register = (req, res) => {
  const { username, password } = req.body;
  const hashedPassword = bcrypt.hashSync(password, 10);

  User.create(username, hashedPassword, (err, result) => {
    if (err) return res.status(500).json(err);
    res.status(201).json({ message: 'User created successfully!',result });
  });
};

const login = (req, res) => {
  const { username, password } = req.body;

  User.findByUsername(username, (err, user) => {
    if (err || !user) return res.status(404).json({ message: 'User not found!' });

    const validPassword = bcrypt.compareSync(password, user.password);
    if (!validPassword) return res.status(401).json({ message: 'Invalid password!' });

    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET);
    res.json({ token });
  });
};

module.exports = { register, login };
