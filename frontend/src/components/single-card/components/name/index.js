import React from "react";
import styles from "./styles.module.css";

export function ComponentName({ name }) {
    return <span className={styles.name}>{name}</span>;
} 