import React from "react";
import styles from "./styles.module.css";

export function ComponentAmount({ amount, measurement_unit }) {
    return (
        <div className={styles.amount}>
            <span className={styles.value}>{amount}</span>
            <span className={styles.unit}>{measurement_unit}</span>
        </div>
    );
} 