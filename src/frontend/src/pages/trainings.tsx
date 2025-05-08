import ChatInterface from "../components/ChatInterface";
import { TrainingList } from "../components/TrainingList";
import CreateTrainingButton from "../components/CreateTrainingButton";
import styles from "./trainings.module.css";
import { useUser } from "../features/UserContext";

export function Trainings() {
    const { username, isLoggedIn } = useUser();
    return (
        <div className={styles["trainings-page"]}>
            <h1>Trainings</h1>
            {isLoggedIn && username && <p>Welcome, {username}!</p>}
            
            {/* Current training */}
            <TrainingList 
                title="Current Training" 
                endpoint="http://localhost:8080/training"
                field="Sailing"
            />
            
            {/* All trainings */}
            <TrainingList 
                title="All Trainings" 
                endpoint="http://localhost:8080/training"
                field="Other"
            />
            <CreateTrainingButton />
            
            <ChatInterface />
        </div>
    );
}
