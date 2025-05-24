import React from 'react';
import styles from './styles.module.css';

const ComponentErrorComponentNameInputContainer = ({ message }) => {
    return <div className={styles.error}>{message}</div>;
};

export default ComponentErrorComponentNameInputContainer; 