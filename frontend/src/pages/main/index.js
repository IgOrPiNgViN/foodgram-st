import { Card, Title, Pagination, CardList, Container, Main, CheckboxGroup } from '../../components'
import styles from './styles.module.css'
import { useDishes } from '../../utils/index.js'
import { useEffect } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'

const HomePage = ({ updateOrders }) => {
  const {
    dishes,
    setDishes,
    dishesCount,
    setDishesCount,
    dishesPage,
    setDishesPage,
    handleLike,
    handleAddToCart
  } = useDishes()

  const getDishes = ({ page = 1 }) => {
    api
      .getDishes({ page })
      .then(res => {
        const { results, count } = res
        setDishes(results)
        setDishesCount(count)
      })
  }

  useEffect(_ => {
    getDishes({ page: dishesPage })
  }, [dishesPage])


  return <Main>
    <Container>
      <MetaTags>
        <title>Рецепты</title>
        <meta name="description" content="Фудграм - Рецепты" />
        <meta property="og:title" content="Рецепты" />
      </MetaTags>
      <div className={styles.title}>
        <Title title='Рецепты' />
      </div>
      {dishes.length > 0 && <CardList>
        {dishes.map(dish => <Card
          {...dish}
          key={dish.id}
          updateOrders={updateOrders}
          handleLike={handleLike}
          handleAddToCart={handleAddToCart}
        />)}
      </CardList>}
      <Pagination
        count={dishesCount}
        limit={6}
        page={dishesPage}
        onPageChange={page => setDishesPage(page)}
      />
    </Container>
  </Main>
}

export default HomePage

