import React from "react";
import { Component } from "../";
import styles from "./styles.module.css";

export function ComponentList({ components, onDelete }) {
    return (
        <div className={styles.list}>
            <h2 className={styles.title}>Компоненты</h2>
            <ul className={styles.items}>
                {components.map((component) => (
                    <Component
                        key={component.id}
                        component={component}
                        onDelete={onDelete}
                    />
                ))}
            </ul>
        </div>
    );
} 