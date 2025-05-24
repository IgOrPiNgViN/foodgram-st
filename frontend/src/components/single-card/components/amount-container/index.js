import React from "react";
import { ComponentAmountLabel } from "../amount-label";
import { ComponentAmountInput } from "../amount-input";
import styles from "./styles.module.css";

export function ComponentAmountContainer({ value, onChange }) {
    return (
        <div className={styles.container}>
            <ComponentAmountLabel>Количество</ComponentAmountLabel>
            <ComponentAmountInput value={value} onChange={onChange} />
        </div>
    );
} 