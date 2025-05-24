import React from "react";
import styles from "./styles.module.css";

export function ComponentErrorComponentListItemNameLabel({ message }) {
    return <div className={styles.error}>{message}</div>;
} 