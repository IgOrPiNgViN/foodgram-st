import React from "react";
import styles from "./styles.module.css";

export function ComponentAmountLabel({ children }) {
    return <label className={styles.label}>{children}</label>;
} 