import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function EditProductPage() {
  const { id } = useParams(); // Get product ID from URL
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { token } = useAuth();

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/products/${id}`);
        setName(response.data.name);
        setDescription(response.data.description);
        setPrice(response.data.price.toString()); // Convert number to string for input
      } catch (err) {
        console.error("Error fetching product for edit:", err);
        setError("Failed to load product for editing.");
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError(null);

    try {
      const response = await axios.put(
        `${import.meta.env.VITE_API_BASE_URL}/products/${id}`,
        { name, description, price: parseFloat(price) },
        {
          headers: {
            Authorization: `Bearer ${token}` //
          }
        }
      );
      setMessage(`Product "${response.data.name}" updated successfully!`);
      // Optionally navigate back to products page
      navigate('/products');
    } catch (err) {
      console.error("Error updating product:", err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(`Failed to update product: ${err.response.data.error}`);
      } else {
        setError('Failed to update product. Please check your input or permissions.');
      }
    }
  };

  if (loading) return <p>Loading product details...</p>;
  if (error) return <p className="error-message">{error}</p>;

  return (
    <div className="page-container">
      <h1>Edit Product</h1>
      <form onSubmit={handleSubmit} className="form-card">
        {/* ... (Same input fields as AddProductPage but pre-filled) */}
        <div className="form-group">
          <label htmlFor="name">Product Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          ></textarea>
        </div>
        <div className="form-group">
          <label htmlFor="price">Price:</label>
          <input
            type="number"
            id="price"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            step="0.01"
            required
          />
        </div>
        <button type="submit" className="button primary">Update Product</button>
        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
      </form>
    </div>
  );
}

export default EditProductPage;