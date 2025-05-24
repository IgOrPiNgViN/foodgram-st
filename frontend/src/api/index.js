import { API_URL } from "../config";

class Api {
  constructor({ baseUrl, headers }) {
    this._baseUrl = baseUrl;
    this._headers = headers;
  }

  _checkResponse(res) {
    if (res.ok) {
      return res.json();
    }
    return Promise.reject(`Ошибка: ${res.status}`);
  }

  _request(url, options) {
    return fetch(url, options).then(this._checkResponse);
  }

  getDishes({ page = 1, author = null }) {
    const url = new URL(`${this._baseUrl}/api/dishes/`);
    url.searchParams.append("page", page);
    if (author) {
      url.searchParams.append("author", author);
    }
    return this._request(url, {
      headers: this._headers,
    });
  }

  getDish({ id }) {
    return this._request(`${this._baseUrl}/api/dishes/${id}/`, {
      headers: this._headers,
    });
  }

  createDish(data) {
    return this._request(`${this._baseUrl}/api/dishes/`, {
      method: "POST",
      headers: this._headers,
      body: data,
    });
  }

  updateDish({ id, data }) {
    return this._request(`${this._baseUrl}/api/dishes/${id}/`, {
      method: "PATCH",
      headers: this._headers,
      body: data,
    });
  }

  deleteDish({ id }) {
    return this._request(`${this._baseUrl}/api/dishes/${id}/`, {
      method: "DELETE",
      headers: this._headers,
    });
  }

  copyDishLink({ id }) {
    return this._request(`${this._baseUrl}/api/dishes/${id}/get-link/`, {
      headers: this._headers,
    });
  }

  getComponents({ name = "" }) {
    const url = new URL(`${this._baseUrl}/api/components/`);
    if (name) {
      url.searchParams.append("name", name);
    }
    return this._request(url, {
      headers: this._headers,
    });
  }

  getComponent({ id }) {
    return this._request(`${this._baseUrl}/api/components/${id}/`, {
      headers: this._headers,
    });
  }

  createComponent(data) {
    return this._request(`${this._baseUrl}/api/components/`, {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify(data),
    });
  }

  updateComponent({ id, data }) {
    return this._request(`${this._baseUrl}/api/components/${id}/`, {
      method: "PATCH",
      headers: this._headers,
      body: JSON.stringify(data),
    });
  }

  deleteComponent({ id }) {
    return this._request(`${this._baseUrl}/api/components/${id}/`, {
      method: "DELETE",
      headers: this._headers,
    });
  }

  getUser({ id }) {
    return this._request(`${this._baseUrl}/api/users/${id}/`, {
      headers: this._headers,
    });
  }

  getUsers({ page = 1 }) {
    const url = new URL(`${this._baseUrl}/api/users/`);
    url.searchParams.append("page", page);
    return this._request(url, {
      headers: this._headers,
    });
  }

  subscribe({ id }) {
    return this._request(`${this._baseUrl}/api/users/${id}/subscribe/`, {
      method: "POST",
      headers: this._headers,
    });
  }

  unsubscribe({ id }) {
    return this._request(`${this._baseUrl}/api/users/${id}/subscribe/`, {
      method: "DELETE",
      headers: this._headers,
    });
  }

  getSubscriptions({ page = 1 }) {
    const url = new URL(`${this._baseUrl}/api/users/subscriptions/`);
    url.searchParams.append("page", page);
    return this._request(url, {
      headers: this._headers,
    });
  }

  getFavorites({ page = 1 }) {
    const url = new URL(`${this._baseUrl}/api/dishes/favorite/`);
    url.searchParams.append("page", page);
    return this._request(url, {
      headers: this._headers,
    });
  }

  addToFavorites({ id }) {
    return this._request(`${this._baseUrl}/api/dishes/${id}/favorite/`, {
      method: "POST",
      headers: this._headers,
    });
  }

  removeFromFavorites({ id }) {
    return this._request(`${this._baseUrl}/api/dishes/${id}/favorite/`, {
      method: "DELETE",
      headers: this._headers,
    });
  }

  getShoppingCart() {
    return this._request(`${this._baseUrl}/api/dishes/shopping_cart/`, {
      headers: this._headers,
    });
  }

  addToShoppingCart({ id }) {
    return this._request(`${this._baseUrl}/api/dishes/${id}/shopping_cart/`, {
      method: "POST",
      headers: this._headers,
    });
  }

  removeFromShoppingCart({ id }) {
    return this._request(`${this._baseUrl}/api/dishes/${id}/shopping_cart/`, {
      method: "DELETE",
      headers: this._headers,
    });
  }

  downloadShoppingCart() {
    return this._request(`${this._baseUrl}/api/dishes/shopping_cart/download/`, {
      headers: this._headers,
    });
  }

  login({ email, password }) {
    return this._request(`${this._baseUrl}/api/auth/token/login/`, {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({ email, password }),
    });
  }

  register({ email, username, first_name, last_name, password }) {
    return this._request(`${this._baseUrl}/api/users/`, {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({
        email,
        username,
        first_name,
        last_name,
        password,
      }),
    });
  }

  logout() {
    return this._request(`${this._baseUrl}/api/auth/token/logout/`, {
      method: "POST",
      headers: this._headers,
    });
  }

  resetPassword({ email }) {
    return this._request(`${this._baseUrl}/api/users/reset_password/`, {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({ email }),
    });
  }

  resetPasswordConfirm({ uid, token, new_password }) {
    return this._request(`${this._baseUrl}/api/users/reset_password_confirm/`, {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({ uid, token, new_password }),
    });
  }

  setToken(token) {
    this._headers["Authorization"] = `Token ${token}`;
  }

  removeToken() {
    delete this._headers["Authorization"];
  }
}

const api = new Api({
  baseUrl: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
