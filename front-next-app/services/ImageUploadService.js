const ImageUploadService = {
    async uploadImages(images) {
      const formData = new FormData();
      images.forEach((image) => {
        formData.append('images', image);
      });

      const apiUrl = process.env.NEXT_PUBLIC_FLASK_PUBLIC_API_URL;  // Fetch the base URL
      //console.log('api url', apiUrl)
  
      const response = await fetch(`${apiUrl}/remove-background`, {
        method: 'POST',
        body: formData,
      });
  
      if (!response.ok) {
        throw new Error('Failed to upload images');
      }
  
      const data = await response.json();
      return data.files; // Assuming this returns processed image URLs
    },
  
    async downloadImage(image) {
      const baseUrl = process.env.NEXT_PUBLIC_FLASK_PUBLIC_URL

      const backUrl = baseUrl;  // Fetch the base URL
      const imageUrl = `${backUrl}${image}`;
      const response = await fetch(imageUrl);
      if (!response.ok) {
        throw new Error('Failed to download image');
      }
  
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
  
      const a = document.createElement('a');
      a.href = url;
      a.download = image;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
  };
  
  export default ImageUploadService;
  