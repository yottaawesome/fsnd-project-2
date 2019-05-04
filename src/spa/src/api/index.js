import ApiTest from "../ui-components/api-test";

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

    static createNewBook(name, description, web_link) {
        return fetch('/bookshelf/', {
            credentials: 'same-origin',
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                name: 'testname',
                description: 'testdescription',
                web_link: 'testweblink'
            })
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

    static editBook(id, name, description, web_link) {
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
                web_link: web_link
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
