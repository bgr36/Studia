import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext'; // Potrzebne do dodawania/usuwania recenzji

function ReviewsPage() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { isAuthenticated, token, userRole, userId: currentUserId } = useAuth(); // Pobierz userId zalogowanego użytkownika

  // State dla nowego formularza recenzji
  const [newReviewRating, setNewReviewRating] = useState('');
  const [newReviewComment, setNewReviewComment] = useState('');
  const [newReviewProductId, setNewReviewProductId] = useState('');
  const [reviewMessage, setReviewMessage] = useState('');

  // --- Funkcja do pobierania recenzji ---
  const fetchReviews = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/reviews`);
      setReviews(response.data);
    } catch (err) {
      console.error("Error fetching reviews:", err);
      setError("Failed to load reviews. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  // --- Funkcja do dodawania nowej recenzji ---
  const handleAddReview = async (e) => {
    e.preventDefault();
    setReviewMessage('');
    setError(null);
    if (!isAuthenticated) {
      setReviewMessage('You must be logged in to add a review.');
      return;
    }
    if (!newReviewProductId || !newReviewRating) {
        setReviewMessage('Product ID and Rating are required.');
        return;
    }
    if (newReviewRating < 1 || newReviewRating > 5) {
        setReviewMessage('Rating must be between 1 and 5.');
        return;
    }

    try {
      await axios.post(`${import.meta.env.VITE_API_BASE_URL}/reviews`,
        {
          rating: parseInt(newReviewRating),
          comment: newReviewComment,
          productId: parseInt(newReviewProductId)
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      setReviewMessage('Review added successfully!');
      setNewReviewRating('');
      setNewReviewComment('');
      setNewReviewProductId('');
      fetchReviews(); // Odśwież listę recenzji
    } catch (err) {
      console.error("Error adding review:", err);
      // Lepsza obsługa błędów z backendu
      const apiErrorMessage = err.response?.data?.details || err.response?.data?.error || err.message;
      setReviewMessage(`Failed to add review: ${apiErrorMessage}`);
    }
  };

  // --- Funkcja do usuwania recenzji ---
  const handleDeleteReview = async (reviewId) => {
    if (!window.confirm("Are you sure you want to delete this review?")) {
      return;
    }
    setReviewMessage('');
    setError(null);
    try {
      await axios.delete(`${import.meta.env.VITE_API_BASE_URL}/reviews/${reviewId}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setReviewMessage('Review deleted successfully!');
      fetchReviews(); // Odśwież listę
    } catch (err) {
      console.error("Error deleting review:", err);
      const apiErrorMessage = err.response?.data?.message || err.response?.data?.error || err.message;
      setError(`Failed to delete review: ${apiErrorMessage}`);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  if (loading) return <p>Loading reviews...</p>;
  if (error) return <p className="error-message">{error}</p>;

  return (
    <div className="page-container">
      <h1>Customer Reviews</h1>

      {/* Formularz dodawania recenzji */}
      {isAuthenticated && (
        <div className="form-card" style={{ marginBottom: '30px' }}>
          <h2>Add a New Review</h2>
          <form onSubmit={handleAddReview}>
            <div className="form-group">
              <label htmlFor="productId">Product ID:</label>
              <input
                type="number"
                id="productId"
                value={newReviewProductId}
                onChange={(e) => setNewReviewProductId(e.target.value)}
                placeholder="E.g., 1, 2, 3"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="rating">Rating (1-5):</label>
              <input
                type="number"
                id="rating"
                value={newReviewRating}
                onChange={(e) => setNewReviewRating(e.target.value)}
                min="1"
                max="5"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="comment">Comment:</label>
              <textarea
                id="comment"
                value={newReviewComment}
                onChange={(e) => setNewReviewComment(e.target.value)}
                placeholder="Enter your comment here"
              ></textarea>
            </div>
            <button type="submit" className="button primary">Submit Review</button>
            {reviewMessage && <p className={reviewMessage.includes('successfully') ? 'success-message' : 'error-message'}>{reviewMessage}</p>}
          </form>
        </div>
      )}

      {/* Lista recenzji */}
      <div className="review-list">
        {reviews.length > 0 ? (
          reviews.map(review => (
            <div key={review.id} className="review-card">
              <p><strong>Rating: {review.rating}/5</strong></p>
              <p>{review.comment}</p>
              {/* Wyświetl dane użytkownika i produktu, jeśli istnieją */}
              {review.user && <p>By: {review.user.username}</p>}
              {review.product && <p>For: {review.product.name}</p>}
              {/* Przycisk usuwania dla admina lub właściciela recenzji */}
              {(isAuthenticated && (userRole === 'admin' || currentUserId === review.userId)) && (
                <button
                  onClick={() => handleDeleteReview(review.id)}
                  className="button danger"
                  style={{ marginTop: '10px' }}
                >
                  Delete Review
                </button>
              )}
            </div>
          ))
        ) : (<p>Empty</p>)}
      </div>
    </div>
  );
}

export default ReviewsPage;