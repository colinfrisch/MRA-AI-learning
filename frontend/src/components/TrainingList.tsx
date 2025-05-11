import { useCallback, useEffect } from "react";
import axios, { AxiosResponse } from "axios";
import { useState } from "react";
import styles from "./TrainingList.module.css";

// Define TrainingResponse interface outside the component for reusability
export interface TrainingResponse {
  id: number;
  name: string;
  field: string;
}

interface TrainingListProps {
  title?: string;
  endpoint: string;
  field?: string;
}

export function TrainingList({ title = "Current Training", endpoint, field }: TrainingListProps) {
  const [trainings, setTrainings] = useState<TrainingResponse[]>([]);

  const fetchTrainings = useCallback(async () => {
    try {
      const url = field
        ? `${endpoint}?field=${encodeURIComponent(field)}`
        : endpoint;

      const response: AxiosResponse<TrainingResponse[]> = await axios.get(url);
      setTrainings(Array.isArray(response.data) ? response.data : [response.data]);
    } catch (error) {
      console.error('Failed to fetch trainings:', error);
    }
  }, [endpoint, field]);

  // Use useEffect with empty dependency array to ensure the API is only called once
  useEffect(() => {
    fetchTrainings();
  }, [fetchTrainings]);

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>{title}</h2>
      <div className={styles.trainingList}>
        {trainings.length > 0 ? (
          trainings.map((training) => (
            <div key={training.id} className={styles.trainingItem}>
              <h3>{training.name}</h3>
              <p>Field: {training.field}</p>
              <p>ID: {training.id}</p>
            </div>
          ))
        ) : (
          <p>No trainings found</p>
        )}
      </div>
    </div>
  );
}
