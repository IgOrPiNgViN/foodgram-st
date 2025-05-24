import React from 'react';
import styles from './styles.module.css';

const ComponentErrorComponent = ({ message }) => {
    return <div className={styles.error}>{message}</div>;
};

export default ComponentErrorComponent; 