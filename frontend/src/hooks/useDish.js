import { useState, useCallback } from "react";
import api from "../api";

export function useDish() {
    const [dish, setDish] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const getDish = useCallback(async ({ id }) => {
        setIsLoading(true);
        setError(null);
        try {
            const data = await api.getDish({ id });
            setDish(data);
        } catch (err) {
            setError(err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    return { dish, isLoading, error, getDish };
} 