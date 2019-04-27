import { AppState } from 'brainlet';

const GlobalState = new AppState();

class LoginState {
    constructor(name, email, method) {
        this.name = name;
        this.email = email;
        this.method = method;
    }
}

/**
 * Represents the Events components can subscribe and unsubscribe from.
 */
const Events = {
    LOGIN: "onAppEventLogin",
    LOGOUT: "onAppEventLogout",
}

/**
 * Represents all State variables that can have data associated with them.
 */
const State = {
    CURRENT_USER: "stateCurrentUser"
}

export { GlobalState, Events, State }
