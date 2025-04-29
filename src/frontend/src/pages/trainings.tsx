import ChatInterface from "../components/ChatInterface";
import { TrainingList } from "../components/TrainingList";
import styles from "./trainings.module.css";

export function Trainings() {
    return (
        <div className={styles["trainings-page"]}>
            <h1>Trainings</h1>
            
            {/* Sailing trainings */}
            <TrainingList 
                title="Current Training" 
                endpoint="http://localhost:8080/training"
                field="Sailing"
            />
            
            {/* Running trainings */}
            <TrainingList 
                title="All Trainings" 
                endpoint="http://localhost:8080/training"
                field="Other"
            />
            
            <ChatInterface />
        </div>
    );
}
