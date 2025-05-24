import React, { useState, useCallback, useEffect } from "react";
import { useTags } from './index.js'
import api from '../api'

export default function useDishes() {
  const [dishes, setDishes] = useState([])
  const [dishesCount, setDishesCount] = useState(0)
  const [dishesPage, setDishesPage] = useState(1)
  const [dishesLimit, setDishesLimit] = useState(6)
  const [dishesAuthor, setDishesAuthor] = useState(null)
  const [dishesTags, setDishesTags] = useState([])
  const [dishesSearch, setDishesSearch] = useState('')
  const [dishesIsFavorited, setDishesIsFavorited] = useState(false)
  const [dishesIsInShoppingCart, setDishesIsInShoppingCart] = useState(false)
  const [dishesIsSubscribed, setDishesIsSubscribed] = useState(false)
  const [dishesIsLoading, setDishesIsLoading] = useState(false)
  const [dishesError, setDishesError] = useState(null)

  const fetchDishes = useCallback(() => {
    setDishesIsLoading(true)
    api.getDishes({
      page: dishesPage,
      limit: dishesLimit,
      author: dishesAuthor,
      tags: dishesTags,
      search: dishesSearch,
      is_favorited: dishesIsFavorited,
      is_in_shopping_cart: dishesIsInShoppingCart,
      is_subscribed: dishesIsSubscribed,
    }).then((dishes) => {
      setDishes(dishes.results)
      setDishesCount(dishes.count)
      setDishesIsLoading(false)
    }).catch((error) => {
      setDishesError(error)
      setDishesIsLoading(false)
    })
  }, [
    dishesPage,
    dishesLimit,
    dishesAuthor,
    dishesTags,
    dishesSearch,
    dishesIsFavorited,
    dishesIsInShoppingCart,
    dishesIsSubscribed,
  ])

  useEffect(() => {
    fetchDishes()
  }, [fetchDishes])

  const handleLike = ({ id, toLike = true }) => {
    const method = toLike ? api.addToFavorites.bind(api) : api.removeFromFavorites.bind(api)
    method({ id }).then(res => {
      const dishesUpdated = dishes.map(dish => {
        if (dish.id === id) {
          dish.is_favorited = toLike
        }
        return dish
      })
      setDishes(dishesUpdated)
    })
      .catch(err => {
        const { errors } = err
        if (errors) {
          alert(errors)
        }
      })
  }

  const handleAddToCart = ({ id, toAdd = true, callback }) => {
    const method = toAdd ? api.addToOrders.bind(api) : api.removeFromOrders.bind(api)
    method({ id }).then(res => {
      const dishesUpdated = dishes.map(dish => {
        if (dish.id === id) {
          dish.is_in_shopping_cart = toAdd
        }
        return dish
      })
      setDishes(dishesUpdated)
      callback && callback(toAdd)
    })
      .catch(err => {
        const { errors } = err
        if (errors) {
          alert(errors)
        }
      })
  }

  return {
    dishes,
    dishesCount,
    dishesPage,
    dishesLimit,
    dishesAuthor,
    dishesTags,
    dishesSearch,
    dishesIsFavorited,
    dishesIsInShoppingCart,
    dishesIsSubscribed,
    dishesIsLoading,
    dishesError,
    setDishes,
    setDishesCount,
    setDishesPage,
    setDishesLimit,
    setDishesAuthor,
    setDishesTags,
    setDishesSearch,
    setDishesIsFavorited,
    setDishesIsInShoppingCart,
    setDishesIsSubscribed,
    handleLike,
    handleAddToCart,
  }
}
