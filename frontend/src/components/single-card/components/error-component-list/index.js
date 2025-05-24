import React from "react";
import styles from "./styles.module.css";

const ComponentErrorComponentList = ({ message }) => {
    return <div className={styles.error}>{message}</div>;
};

export default ComponentErrorComponentList; 