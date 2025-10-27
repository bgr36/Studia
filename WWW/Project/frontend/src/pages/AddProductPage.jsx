import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function AddProductPage() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { token } = useAuth(); // Get token from AuthContext

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError(null);

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/products`,
        { name, description, price: parseFloat(price) },
        {
          headers: {
            Authorization: `Bearer ${token}` //
          }
        }
      );
      setMessage(`Product "${response.data.name}" added successfully!`);
      setName('');
      setDescription('');
      setPrice('');
      // Optionally navigate to products page or clear form
      navigate('/products');
    } catch (err) {
      console.error("Error adding product:", err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(`Failed to add product: ${err.response.data.error}`);
      } else if (err.response && err.response.data && err.response.data.message) {
         setError(`Failed to add product: ${err.response.data.message}`);
      }
      else {
        setError('Failed to add product. Please check your input.');
      }
    }
  };

  return (
    <div className="page-container">
      <h1>Add New Product</h1>
      <form onSubmit={handleSubmit} className="form-card">
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
        <button type="submit" className="button primary">Add Product</button>
        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
      </form>
    </div>
  );
}

export default AddProductPage;