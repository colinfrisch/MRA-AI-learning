import { createContext, useContext } from "react";

type UserContextType = {
  username: string | null;
  setUsername: (username: string | null) => void;
  isLoggedIn: boolean;
  setIsLoggedIn: (isLoggedIn: boolean) => void;
  inputUsername: string;
  setInputUsername: (username: string) => void;
  phone: string | null;
  setPhone: (phone: string | null) => void;
};

export const UserContext = createContext<UserContextType | undefined>(undefined);

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used within a UserProvider");
  return context;
};
