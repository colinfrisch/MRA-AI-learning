import styles from './header.module.css';
import { useNavigate } from 'react-router-dom';

function Header() {
    const navigate = useNavigate();
    return (
        <header className={styles.header}>
            <div className={styles.toolbar}>
                <button className={styles.button} onClick={() => navigate('/')}>HOME</button>
                <button className={styles.button} onClick={() => navigate('/trainings')}>TRAININGS</button>
            </div>
        </header>
    );
}

export default Header;