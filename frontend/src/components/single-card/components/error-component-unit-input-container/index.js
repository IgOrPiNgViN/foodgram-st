import React from 'react';
import styles from './styles.module.css';

const ComponentErrorComponentUnitInputContainer = ({ message }) => {
    return <div className={styles.error}>{message}</div>;
};

export default ComponentErrorComponentUnitInputContainer; 