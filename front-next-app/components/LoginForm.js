import { useState, useContext } from 'react';
import { login_user } from '../services/authService';
import AuthContext from '../contexts/AuthContext';
import { useRouter } from 'next/router';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login: setAuthToken } = useContext(AuthContext);
  const router = useRouter();

  //console.log("yes",AuthContext)

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = await login_user(username, password);
      //console.log(login);
      setAuthToken(token); // Save token to context and localStorage
      router.push('/dashboard'); // Redirect to dashboard
    } catch (err) {
      setError('Invalid credentials');
      console.log(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      {error && <p>{error}</p>}
      <div>
        <label>Email:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
