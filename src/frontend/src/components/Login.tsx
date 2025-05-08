import { useState } from 'react';
import axios from 'axios';
import styles from './Login.module.css';
import { useUser } from '../features/UserContext';

export function Login() {
  const { 
    setUsername, 
    setIsLoggedIn, 
    inputUsername, 
    setInputUsername,
    isLoggedIn 
  } = useUser();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8080/login', { username: inputUsername });
      console.log('Login success:', response.data);
      // Only set the username and logged in state after successful login
      setUsername(inputUsername);
      setIsLoggedIn(true);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleLogout = () => {
    setUsername(null);
    setIsLoggedIn(false);
    setInputUsername('');
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
        <button type="submit" className={styles.button}>Login</button>
      </form>
    </div>
  );
}
