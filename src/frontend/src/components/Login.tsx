import { useState } from 'react';
import axios from 'axios';
import styles from './Login.module.css';
import { useUser } from '../features/UserContext';

export function Login() {
  const { 
    setUsername,
    isLoggedIn, 
    setIsLoggedIn, 
    inputUsername, 
    setInputUsername,
    phone,
    setPhone
  } = useUser();

  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post('http://localhost:8080/login', { 
        username: inputUsername,
        phone: phone
      });
      console.log('Login success:', response.data);
      // Set all user data from response
      setUsername(response.data.username);
      setPhone(response.data.phone);
      setIsLoggedIn(true);
    } catch (error: any) {
      console.error('Login failed:', error);
      setError(error.response?.data?.error || 'Login failed');
    }
  };

  const handleLogout = () => {
    setUsername(null);
    setIsLoggedIn(false);
    setInputUsername('');
    setPhone(null);
    setError('');
  };

  if (isLoggedIn) {
    return (
      <div className={styles.container}>
        <button onClick={handleLogout} className={styles.button}>Logout</button>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <form onSubmit={handleLogin} className={styles.form}>
        <input 
          type="text" 
          value={inputUsername}
          onChange={(e) => setInputUsername(e.target.value)}
          placeholder="Enter username"
          className={styles.input}
        />
        <input 
          type="tel" 
          value={phone || ''}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="Enter phone number"
          className={styles.input}
        />
        {error && <div className={styles.error}>{error}</div>}
        <button type="submit" className={styles.button}>Login</button>
      </form>
    </div>
  );
}
