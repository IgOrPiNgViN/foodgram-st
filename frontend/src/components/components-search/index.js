import React, { useState, useEffect } from "react";
import api from "../../api";
import styles from "./styles.module.css";

export function ComponentsSearch({ onSelect }) {
    const [search, setSearch] = useState("");
    const [components, setComponents] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const searchComponents = async () => {
            if (search.length < 2) {
                setComponents([]);
                return;
            }

            setIsLoading(true);
            setError(null);
            try {
                const data = await api.getComponents({ name: search });
                setComponents(data);
            } catch (err) {
                setError(err);
            } finally {
                setIsLoading(false);
            }
        };

        const timeoutId = setTimeout(searchComponents, 300);
        return () => clearTimeout(timeoutId);
    }, [search]);

    const handleSelect = (component) => {
        onSelect(component);
        setSearch("");
        setComponents([]);
    };

    return (
        <div className={styles.search}>
            <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Поиск компонентов..."
                className={styles.input}
            />
            {isLoading && <div className={styles.loading}>Загрузка...</div>}
            {error && <div className={styles.error}>Ошибка: {error.message}</div>}
            {components.length > 0 && (
                <ul className={styles.list}>
                    {components.map((component) => (
                        <li
                            key={component.id}
                            onClick={() => handleSelect(component)}
                            className={styles.item}
                        >
                            {component.name}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
} 