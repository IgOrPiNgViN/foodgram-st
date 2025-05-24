import React from "react";
import styles from "./styles.module.css";

export function ComponentAmountInput({ value, onChange }) {
    return (
        <div className={styles.input}>
            <input
                type="number"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                min="1"
                step="1"
                className={styles.field}
            />
        </div>
    );
} 