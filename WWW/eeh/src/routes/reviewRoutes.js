const express = require('express');
const router = express.Router();
const ctrl = require('../controllers/reviewController');
const { authenticate, authorize } = require('../middleware/auth');

router.get('/', authenticate, ctrl.list);
router.post('/', authenticate, ctrl.create);
router.get('/:id', authenticate, ctrl.get);
router.put('/:id', authenticate, authorize('admin'), ctrl.update);
router.delete('/:id', authenticate, authorize('admin'), ctrl.remove);

module.exports = router;