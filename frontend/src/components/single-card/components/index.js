import React from "react";
import { ComponentDelete } from "../../icons";
import styles from "./styles.module.css";

export function Component({ component, onDelete }) {
    const { id, name, amount, measurement_unit } = component;

    return (
        <li className={styles.component}>
            <span className={styles.name}>{name}</span>
            <span className={styles.amount}>
                {amount} {measurement_unit}
            </span>
            <button className={styles.delete} onClick={() => onDelete(id)}>
                <ComponentDelete />
            </button>
        </li>
    );
} 