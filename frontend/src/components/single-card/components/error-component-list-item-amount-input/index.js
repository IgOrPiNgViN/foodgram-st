import React from "react";
import styles from "./styles.module.css";

export function ComponentErrorComponentListItemAmountInput({ message }) {
  return <div className={styles.error}>{message}</div>;
} 