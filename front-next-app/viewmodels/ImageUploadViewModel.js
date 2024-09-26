import { useState } from 'react';
import ImageUploadService from '../services/ImageUploadService';

const ImageUploadViewModel = () => {
  const [selectedImages, setSelectedImages] = useState([]);
  const [processedImages, setProcessedImages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleImageChange = async (event) => {
    if (event.target.files) {
      const newImages = Array.from(event.target.files);
      setSelectedImages((prevImages) => [...prevImages, ...newImages]);
      await uploadImages(newImages);
    }
  };

  const uploadImages = async (images) => {
    setLoading(true);
    try {
      const newProcessedImages = await ImageUploadService.uploadImages(images);
      setProcessedImages((prevImages) => [...prevImages, ...newProcessedImages]);
    } catch (error) {
      console.error('Error uploading images:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageRemove = (index) => {
    setSelectedImages((prevImages) => prevImages.filter((_, i) => i !== index));
    setProcessedImages((prevImages) => prevImages.filter((_, i) => i !== index));
  };

  const handleImageDownload = async (image) => {
    await ImageUploadService.downloadImage(image);
  };

  return {
    selectedImages,
    processedImages,
    loading,
    handleImageChange,
    handleImageRemove,
    handleImageDownload,
  };
};

export default ImageUploadViewModel;
