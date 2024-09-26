import { useState } from 'react';
import { Button, Card } from 'flowbite-react';

const ImageUpload = () => {
  const [selectedImages, setSelectedImages] = useState([]);
  // Store processed images
  const [processedImages, setProcessedImages] = useState([]); 

  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);




  const handleImageChange = async(event) => {
    if (event.target.files) {
      const newImages = Array.from(event.target.files);
      setSelectedImages((prevImages) => [...prevImages, ...newImages]);
      await uploadImages(newImages);
    }
  };

  const uploadImages = async (images) => {
    const formData = new FormData();
    images.forEach((image) => {
      formData.append('images', image);
    });

    try {
        setLoading(true); 
      const response = await fetch('http://localhost:5000/api/v1/remove-background', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload images');
      }

      const data = await response.json();
      //console.log('Response from API:', data);
      // Handle the response from the API as needed

      // Assuming the API returns an array of processed image URLs or base64 strings
      const newProcessedImages = data.files; // Update based on API response structure
      setProcessedImages((prevImages) => [...prevImages, ...newProcessedImages]);

    } catch (error) {
      console.error('Error uploading images:', error);
    } finally {
        setLoading(false);
    }
  };

  const handleImageRemove = (index) => {
    setSelectedImages((prevImages) =>
      prevImages.filter((_, i) => i !== index)
    );
    setProcessedImages((prevImages) => prevImages.filter((_, i) => i !== index));

  };

  const handleImageDownload = async (image) => {
    const imageUrl = `http://localhost:5000/${image}`; // Full URL of the image
  
    try {
      const response = await fetch(imageUrl);
      if (!response.ok) {
        throw new Error('Failed to download image');
      }
  
      const blob = await response.blob(); // Get image as a blob
      const url = window.URL.createObjectURL(blob); // Create URL from blob
  
      const a = document.createElement('a');
      a.href = url;
      a.download = image; // Set the name for the downloaded file
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading image:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <h2 className="text-3xl font-extrabold text-gray-900 mb-6">
        Upload for remove background
      </h2>
      {loading && (
        <div className="flex flex-col items-center justify-center mt-6">
            <svg className="animate-spin h-8 w-8 text-gray-900 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8h8a8 8 0 01-8 8 8 8 0 01-8-8z"></path>
            </svg>
            <p className="text-gray-500 mb-2">Processing images...</p>
        </div>
        )}

      {/* Dropzone Area */}
      {!loading && (
      <div className="flex items-center justify-center w-full">
        <label
          htmlFor="dropzone-file"
          className="flex flex-col items-center justify-center w-full max-w-lg h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600 relative"
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <svg
              className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 16"
              aria-hidden="true"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
              />
            </svg>
            <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
              <span className="font-semibold">Click to upload</span> or drag and
              drop
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
                PNG, JPG, JPEG or GIF (MAX. 800x400px)
            </p>
          </div>
          <input
            id="dropzone-file"
            type="file"
            //className="hidden"
            className="absolute top-0 left-0 w-full h-full opacity-0 cursor-pointer"
            accept="image/*"
            multiple
            onChange={handleImageChange}
          />
        </label>
      </div>
       )}

      {/* Image Preview with Horizontal Scroll */}
      {processedImages.length > 0 && (
        <div className="mt-6 w-full overflow-x-auto">
          <div className="flex space-x-4 p-4">
            {processedImages.map((image, index) => (
            //   <Card key={index} className="flex-shrink-0 w-32 relative">
            <div key={index} className="flex-shrink-0 w-32 relative">
                <button
                  onClick={() => handleImageRemove(index)}
                  className="absolute top-2 right-2 text-dark rounded-full p-1 text-sm"
                >
                  ×
                </button>
                <button
                  onClick={() => handleImageDownload(image)}
                  className="absolute bottom-2 right-2 w-8 h-8 bg-blue-600 text-white rounded-lg flex items-center justify-center text-sm"
                >
                  ↓
                </button>
                <img
                  src={`http://localhost:5000/${image}`}
                  //src={URL.createObjectURL(image)}
                  width="300px" 
                  height="300px"
                  alt={`Preview ${index}`}
                  className="w-full h-auto border-2 border-gray-300 rounded-lg shadow-md"
                />
            </div>

            //   </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
