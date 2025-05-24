import React from "react";
import { Link } from "react-router-dom";
import { Heart, ShoppingCart, Edit, Delete, Copy } from "../icons";
import styles from "./styles.module.css";

export function SingleCard({ dish, onLike, onAddToCart, onDelete, onCopy }) {
    const { id, name, image, cooking_time, text, author, is_favorited, is_in_shopping_cart } = dish;

    return (
        <div className={styles.card}>
            <div className={styles.header}>
                <h1 className={styles.title}>{name}</h1>
                <div className={styles.actions}>
                    <button className={styles.button} onClick={() => onLike(id)}>
                        <Heart className={is_favorited ? styles.active : ""} />
                    </button>
                    <button className={styles.button} onClick={() => onAddToCart(id)}>
                        <ShoppingCart className={is_in_shopping_cart ? styles.active : ""} />
                    </button>
                    <button className={styles.button} onClick={() => onCopy(id)}>
                        <Copy />
                    </button>
                    {author.is_current_user && (
                        <>
                            <Link to={`/dishes/${id}/edit`} className={styles.button}>
                                <Edit />
                            </Link>
                            <button className={styles.button} onClick={() => onDelete(id)}>
                                <Delete />
                            </button>
                        </>
                    )}
                </div>
            </div>
            <img src={image} alt={name} className={styles.image} />
            <div className={styles.content}>
                <p className={styles.time}>Время приготовления: {cooking_time} мин.</p>
                <p className={styles.text}>{text}</p>
            </div>
        </div>
    );
} 