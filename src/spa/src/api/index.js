export default class ServerApi {
  constructor() {}

  static fetchUserDetails() {
    return fetch('/user/', {
      credentials: 'same-origin'  
    });
  }

  static logout() {
    return fetch('/logout/', {
      credentials: 'same-origin',
      method: "DELETE",
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
  }

  static fetchBookshelf() {
    return fetch('/bookshelf/', {
      credentials: 'same-origin',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
  }

  static fetchBook(id) {
    return fetch(`/book/${id}`, {
      credentials: 'same-origin',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
  }

  static createBook(name, description, web_link, categories) {
    return fetch('/bookshelf/', {
      credentials: 'same-origin',
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        name: name,
        description: description,
        web_link: web_link,
        categories: categories
      })
    });
  }

  static editBook(id, name, description, web_link, categories) {
    return fetch(`/book/${id}`, {
      credentials: 'same-origin',
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        name: name,
        description: description,
        web_link: web_link,
        categories: categories
      })
    });
  }

  static deleteBook(id) {
    return fetch(`/book/${id}`, {
      credentials: 'same-origin',
      method: 'DELETE',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
  }

  static postGoogleAuthCode(state, code) {
    return fetch('/googleauth/', {
      credentials: 'same-origin',
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        code: code,
        state: state
      })
    });
  }
}
