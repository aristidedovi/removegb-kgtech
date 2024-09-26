export const login_user = async (username, password) => {
    const res = await fetch('http://localhost:5000/api/v1/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
  
    if (res.ok) {
      const data = await res.json();
      //console.log(data);
      return data.access_token; // Return the JWT
    } else {
      throw new Error('Invalid credentials');
    }
  };
  