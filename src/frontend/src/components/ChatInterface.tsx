//import { FormEvent, useEffect, useRef, 
import { useState } from 'react';
import styles from './ChatInterface.module.css';
// import axios from 'axios';

function ChatInterface() {
    const [isExpanded, setIsExpanded] = useState(false);

    const toggleChat = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <div className={`${styles.chatInterface} ${isExpanded ? styles.expanded : styles.collapsed}`}>
            <div className={styles.chatToggle} onClick={toggleChat}>
                {isExpanded ? 'Hide Chat' : 'Open Chat'}
            </div>
            {isExpanded && (
                <>
                    <div className={styles.chatLog}>
                    </div>
                    <form className={styles.chatForm}>
                        <input 
                            type="text" 
                            placeholder="Chat with MRA"
                            className={styles.messageInput}
                            required 
                        />
                        <button type="submit" className={styles.sendButton}>Send</button>
                    </form>
                </>
            )}
        </div>
    );
}

export default ChatInterface;