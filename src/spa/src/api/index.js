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
            method: "DELETE"
        });
    }

    static fetchBookshelf() {
        return fetch('/bookshelf/', {
            credentials: 'same-origin',
        })
    }

    static createNewBook() {
        return fetch('/bookshelf/', {
            credentials: 'same-origin',
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: 'testname',
                description: 'testdescription',
                weblink: 'testweblink'
            })
        })
    }
}
