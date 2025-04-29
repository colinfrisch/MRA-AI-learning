import { useState } from 'react';
import axios from 'axios';
import styles from './Login.module.css';

export function Login() {
  const [username, setUsername] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8080/login', { username });
      console.log('Login success:', response.data);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className={styles.container}>
      <form onSubmit={handleLogin} className={styles.form}>
        <input 
          type="text" 
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter username"
          className={styles.input}
        />
        <button type="submit" className={styles.button}>Login</button>
      </form>
    </div>
  );
}
