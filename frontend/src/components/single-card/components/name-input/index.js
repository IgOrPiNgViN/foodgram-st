import React from "react";
import styles from "./styles.module.css";

export function ComponentNameInput({ value, onChange }) {
    return (
        <div className={styles.input}>
            <input
                type="text"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder="Название компонента"
                className={styles.field}
            />
        </div>
    );
} 