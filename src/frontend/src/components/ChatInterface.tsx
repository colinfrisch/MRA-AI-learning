import { FormEvent, useRef, useState } from 'react';
import styles from './ChatInterface.module.css';

function ChatInterface() {
    const [messages, setMessages] = useState<string[]>([]);

    const inputRef = useRef<HTMLInputElement>(null);

    const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const userMessage = inputRef.current?.value.trim();
        if (!userMessage) return;
    
        setMessages(prev => [...prev, userMessage]);
    
        if (inputRef.current) {
            inputRef.current.value = '';
        }
    };
    

    return (
        
        <div className={styles.chatInterface}>
            <div className={styles.chatLog}>
            {messages.map((msg, i) => (
                <div key={i} className={styles.chatMessage}>
                {msg}
                </div>
            ))}
            </div>
            <form onSubmit={handleSubmit} className={styles.chatForm}>
                <input 
                    ref={inputRef}
                    type="text" 
                    placeholder="Chat with MRA"
                    className={styles.messageInput}
                    required 
                />
                <button type="submit" className={styles.sendButton}>Send</button>
            </form>
            
        </div>
    );
}

export default ChatInterface;