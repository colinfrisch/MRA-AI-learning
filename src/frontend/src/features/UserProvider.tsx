import { useState, ReactNode } from "react";
import { UserContext } from "./UserContext";

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [username, setUsername] = useState<string | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [inputUsername, setInputUsername] = useState("");
  const [phone, setPhone] = useState<string | null>(null);

  return (
    <UserContext.Provider value={{ 
      username, 
      setUsername, 
      isLoggedIn, 
      setIsLoggedIn,
      inputUsername,
      setInputUsername,
      phone,
      setPhone
    }}>
      {children}
    </UserContext.Provider>
  );
};
