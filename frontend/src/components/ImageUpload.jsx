import React, { useState, useRef } from 'react';
import './ImageUpload.css';

const ImageUpload = ({ onImageUpload, onAnalyze, isLoading }) => {
  const [imagePreview, setImagePreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImagePreview(URL.createObjectURL(file));
      onImageUpload(file);
    }
  };

  const openFileDialog = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="upload-container">
      <div className="upload-box" onClick={openFileDialog}>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          style={{ display: 'none' }}
          ref={fileInputRef}
        />
        {imagePreview ? (
          <img src={imagePreview} alt="Food preview" className="image-preview" />
        ) : (
          <div className="upload-placeholder">
            <p>📸</p>
            <p>Click to Upload an Image</p>
            <span>Upload a photo of your meal</span>
          </div>
        )}
      </div>
      <button onClick={onAnalyze} className="analyze-button" disabled={isLoading || !imagePreview}>
        {isLoading ? 'Analyzing...' : 'Analyze Meal'}
      </button>
    </div>
  );
};

export default ImageUpload;