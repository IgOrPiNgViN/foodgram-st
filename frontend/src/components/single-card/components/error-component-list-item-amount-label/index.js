import React from "react";
import styles from "./styles.module.css";

export function ComponentErrorComponentListItemAmountLabel({ message }) {
    return <div className={styles.error}>{message}</div>;
} 