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
}
