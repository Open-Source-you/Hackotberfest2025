import express from 'express';
import { logout, login ,register, getOtherUsers} from "../controllers/userController.js";
import isAuthenticated from "../middleware/isAuthenticated.js"
const router = express.Router();

router.route('/register').post(register);
router.route('/login').post(login)
router.route('/logout').get(logout)
router.route('/').get(isAuthenticated , getOtherUsers)
export default router;

 

// GET route for /register
// router.get('/register', (req, res) => {
//   res.send('This is the register page');
// });

// export default router;
