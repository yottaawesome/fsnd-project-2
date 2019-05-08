export default class ServerApi {
  constructor() {}

  static fetchUserDetails() {
    return (
      fetch('/user/', {
        credentials: 'same-origin'  
      })
      .then(response => {
        return response.status == 215 ? Promise.reject(response.status) : response.json();
      }));
  }

  static logout() {
    return (
      fetch('/logout/', {
        credentials: 'same-origin',
        method: "DELETE",
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then((response) => {
        return response.status != 204 ? Promise.reject(response.status) : response;
      }));
  }

  static fetchBookshelf() {
    return (
      fetch('/bookshelf/', {
        credentials: 'same-origin',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        return response.status != 200 ? Promise.reject(response.status) : response.json();
      })
    );
  }

  static fetchBook(id) {
    return (
      fetch(`/book/${id}`, {
        credentials: 'same-origin',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        return response.status != 200 ? Promise.reject(response.status) : response.json();
      }));
  }

  static createBook(name, description, web_link, categories) {
    return (
      fetch('/bookshelf/', {
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
      })
      .then(response => {
        return response.status != 200 ? Promise.reject(response.status) : response.json();
      }));
  }

  static editBook(id, name, description, web_link, categories) {
    return (
      fetch(`/book/${id}`, {
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
      })
      .then(response => {
        return response.status != 200 ? Promise.reject(response.status) : response.json();
      }));
  }

  static deleteBook(id) {
    return (
      fetch(`/book/${id}`, {
        credentials: 'same-origin',
        method: 'DELETE',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        return response.status != 204 ? Promise.reject(response.status) : response;
      }));
  }

  static postGoogleAuthCode(state, code) {
    return (
      fetch('/googleauth/', {
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
      }).then(response => {
        return response.status != 200 ? Promise.reject(response.status) : response.json()
      }));
  }

  static fetchCategories() {
    return (
      fetch('/categories/', {
        credentials: 'same-origin',
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        return response.status == 200 ? response.json() : Promise.reject(response.status);
      }));
  }
}
