class LoginState {
    constructor(name, email, method) {
        this.name = name;
        this.email = email;
        this.method = method;
    }
}

const Events = {
    LOGIN: "onAppEventLogin",
    LOGOUT: "onAppEventLogout",
}

const eventSubscription = { }
eventSubscription[Events.LOGIN] = []
eventSubscription[Events.LOGOUT] = []

class AppState {
    static doLoginState(loginState) {
        if(loginState == null)
            throw "loginState cannot be null";
        StateHandler.LoginState = loginState;
    }
    
    static doLogoutState() {
        StateHandler.LoginState = null;
    }

    static isLoggedIn() {
        return StateHandler.LoginState != null;
    }

    static subscribe(obj, ...args) {
        if(obj == null || args.length == 0)
            return;
        for(const eventName of args) {
            if(eventSubscription[eventName] != null && eventSubscription[eventName].find(o => o == obj) == null) {
                eventSubscription[eventName].push(obj);
            }
        }
    }

    static unsubscribe(obj, ...args) {
        if(obj == null)
            return;

        // args is never null
        if(args.length > 0) {
            for(const eventName of args) {
                if(eventSubscription[eventName] != null) {
                    eventSubscription[eventName] = eventSubscription[eventName].filter((val, index, arr) => val != obj);
                    console.log(`Unsubscribed an object for event ${eventName}.`)
                }
            }
        } else {
            let arr = Object.values(Events);
            for(const eventArrayName of arr) {
                eventSubscription[eventArrayName] = eventSubscription[eventArrayName].filter((val, index, arr) => val != obj);
            }
            console.log(`Globally unsubscribed an object for event ${eventArrayName}.`)
        }
    }

    static raiseEvent(event, data) {
        if(event == null)
            return;
        for(const o of eventSubscription[event]) {
            if(o != null && o[event] != null)
                o[event](event, data);
        }
    }
}

export { AppState, Events }
