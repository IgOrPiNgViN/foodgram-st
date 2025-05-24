import React from "react";
import { ComponentDelete } from "../../../icons";
import styles from "./styles.module.css";

export function ComponentDeleteButton({ onDelete }) {
    return (
        <button className={styles.delete} onClick={onDelete}>
            <ComponentDelete />
        </button>
    );
} 