import React from "react";
import styles from "./styles.module.css";

export function ComponentAddButton({ onClick }) {
    return (
        <button className={styles.add} onClick={onClick}>
            Добавить компонент
        </button>
    );
} 