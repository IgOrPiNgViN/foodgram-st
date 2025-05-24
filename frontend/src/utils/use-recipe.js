import React, { useState, useCallback, useEffect } from "react";
import api from '../api'

export default function useDish() {
  const [dish, setDish] = useState({})
  const [dishIsLoading, setDishIsLoading] = useState(false)
  const [dishError, setDishError] = useState(null)

  const fetchDish = useCallback((id) => {
    setDishIsLoading(true)
    api.getDish(id).then((dish) => {
      setDish(dish)
      setDishIsLoading(false)
    }).catch((error) => {
      setDishError(error)
      setDishIsLoading(false)
    })
  }, [])

  useEffect(() => {
    fetchDish()
  }, [fetchDish])

  const handleLike = ({ id, toLike = 1 }) => {
    const method = toLike ? api.addToFavorites.bind(api) : api.removeFromFavorites.bind(api)
    method({ id }).then(res => {
      const dishUpdated = { ...dish, is_favorited: Number(toLike) }
      setDish(dishUpdated)
    })
      .catch(err => {
        const { errors } = err
        if (errors) {
          alert(errors)
        }
      })
  }

  const handleAddToCart = ({ id, toAdd = 1, callback }) => {
    const method = toAdd ? api.addToOrders.bind(api) : api.removeFromOrders.bind(api)
    method({ id }).then(res => {
      const dishUpdated = { ...dish, is_in_shopping_cart: Number(toAdd) }
      setDish(dishUpdated)
      callback && callback(toAdd)
    })
      .catch(err => {
        const { errors } = err
        if (errors) {
          alert(errors)
        }
      })
  }

  const handleSubscribe = ({ author_id, toSubscribe = 1 }) => {
    const method = toSubscribe ? api.subscribe.bind(api) : api.deleteSubscriptions.bind(api)
    method({
      author_id
    })
      .then(_ => {
        const dishUpdated = { ...dish, author: { ...dish.author, is_subscribed: toSubscribe } }
        setDish(dishUpdated)
      })
      .catch(err => {
        const { errors } = err
        if (errors) {
          alert(errors)
        }
      })
  }

  return {
    dish,
    dishIsLoading,
    dishError,
    setDish,
    handleLike,
    handleAddToCart,
    handleSubscribe
  }
}
