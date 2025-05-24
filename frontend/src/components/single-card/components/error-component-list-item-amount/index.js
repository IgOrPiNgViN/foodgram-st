import React from "react";
import styles from "./styles.module.css";

export function ComponentErrorComponentListItemAmount({ message }) {
  return <div className={styles.error}>{message}</div>;
} 