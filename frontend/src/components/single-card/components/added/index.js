import React from "react";
import { Component } from "../";
import styles from "./styles.module.css";

export function ComponentAdded({ components, onDelete }) {
    return (
        <div className={styles.added}>
            <h2 className={styles.title}>Добавленные компоненты</h2>
            <ul className={styles.list}>
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