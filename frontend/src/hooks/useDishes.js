import { useState, useCallback } from "react";
import api from "../api";

export function useDishes() {
    const [dishes, setDishes] = useState([]);
    const [dishesCount, setDishesCount] = useState(0);
    const [dishesPage, setDishesPage] = useState(1);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const getDishes = useCallback(async ({ page = 1, author = null } = {}) => {
        setIsLoading(true);
        setError(null);
        try {
            const data = await api.getDishes({ page, author });
            setDishes(data.results);
            setDishesCount(data.count);
            setDishesPage(page);
        } catch (err) {
            setError(err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    return {
        dishes,
        setDishes,
        dishesCount,
        setDishesCount,
        dishesPage,
        setDishesPage,
        isLoading,
        error,
        getDishes,
    };
} 