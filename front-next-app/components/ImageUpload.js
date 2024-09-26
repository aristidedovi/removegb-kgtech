import React from 'react';
import { Button, Card } from 'flowbite-react';
import ImageUploadViewModel from '../viewmodels/ImageUploadViewModel';
import getConfig from "next/config";

const ImageUpload = () => {
  const { selectedImages, processedImages, loading, handleImageChange, handleImageRemove, handleImageDownload } = ImageUploadViewModel();
  const { serverRuntimeConfig } = getConfig();

  //const apiUrl = process.env.NEXT_PUBLIC_FLASK_PUBLIC_API_URL;  // Fetch the base URL
  //const apiUrl = serverRuntimeConfig.NEXT_PUBLIC_FLASK_PUBLIC_API_URL;  // Fetch the base URL
  //console.log('api url', apiUrl)
  
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

      {!loading && (
        <div className="flex items-center justify-center w-full">
          <label
            htmlFor="dropzone-file"
            className="flex flex-col items-center justify-center w-full max-w-lg h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50"
          >
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <svg className="w-8 h-8 mb-4 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5A5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
              </svg>
              <p className="mb-2 text-sm text-gray-500">
                <span className="font-semibold">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-gray-500">PNG, JPG, JPEG or GIF</p>
            </div>
            <input
              id="dropzone-file"
              type="file"
              className="absolute top-0 left-0 w-full h-full opacity-0 cursor-pointer"
              accept="image/*"
              multiple
              onChange={handleImageChange}
            />
          </label>
        </div>
      )}

      {processedImages.length > 0 && (
        <div className="mt-6 w-full overflow-x-auto">
          <div className="flex space-x-4 p-4">
            {processedImages.map((image, index) => (
              <div key={index} className="flex-shrink-0 w-32 relative">
                <button onClick={() => handleImageRemove(index)} className="absolute top-2 right-2 text-dark rounded-full p-1 text-sm">
                  ×
                </button>
                <button onClick={() => handleImageDownload(image)} className="absolute bottom-2 right-2 w-8 h-8 bg-blue-600 text-white rounded-lg flex items-center justify-center text-sm">
                  ↓
                </button>
                <img src={`${process.env.NEXT_PUBLIC_FLASK_PUBLIC_URL}${image}`} width="300px" height="300px" alt={`Preview ${index}`} className="w-full h-auto border-2 border-gray-300 rounded-lg shadow-md" />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
