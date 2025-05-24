import React from "react";
import styles from "./styles.module.css";

const ComponentErrorComponentListItem = ({ message }) => {
    return <div className={styles.error}>{message}</div>;
};

export default ComponentErrorComponentListItem; 