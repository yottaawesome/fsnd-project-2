export default class ServerApi {
  constructor() {}

  static fetchUserDetails() {
    return (
      fetch('api/v1/user/', {
        credentials: 'same-origin'  
      })
      .then(response => {
        return response.status == 215 ? Promise.reject(response.status) : response.json();
      }));
  }

  static logout() {
    return (
      fetch('api/v1/user/', {
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
      fetch('api/v1/bookshelf/', {
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

  static fetchSortedBookshelf() {
    return (
      fetch('/api/v1/bookshelf/sorted/', {
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
      fetch(`api/v1/book/${id}`, {
        credentials: 'same-origin',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        return response.status != 200 ? Promise.reject(response.status) : response.json();
      }));
  }

  static createBook(book) {
    return (
      fetch('api/v1/bookshelf/', {
        credentials: 'same-origin',
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(book)
      })
      .then(response => {
        return response.status != 200 ? Promise.reject(response.status) : response.json();
      }));
  }

  static editBook(book) {
    let id = book.id;
    delete book.id;
    return (
      fetch(`api/v1/book/${id}`, {
        credentials: 'same-origin',
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(book)
      })
      .then(response => {
        return response.status != 200 ? Promise.reject(response.status) : response.json();
      }));
  }

  static deleteBook(id) {
    return (
      fetch(`api/v1/book/${id}`, {
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
      fetch('api/v1/googleauth/', {
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
      })
      .then(response => {
        return response.status != 200 ? Promise.reject(response.status) : response.json()
      }));
  }

  static fetchCategories() {
    return (
      fetch('api/v1/categories/', {
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

  static fetchApiDoc() {
    return (
      fetch('api/v1/docs/', {
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

  static fetchAuthProviders() {
    return (
      fetch('api/v1/authproviders/', {
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
