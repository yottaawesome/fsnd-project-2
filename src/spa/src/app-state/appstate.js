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

const eventSubscription = { }
eventSubscription[Events.LOGIN] = []
eventSubscription[Events.LOGOUT] = []

/**
 * Represents all State variables that can have data associated with them.
 */
const State = {
    CURRENT_USER: "stateCurrentUser"
}
const eventStateData = {}
eventStateData.CURRENT_USER = null

function required(param="") {
    throw new Error(`A missing parameter was encountered ${param}`);
}

/**
 * Controls basic state and event handling for this application.
 */
class AppState {
    /**
     * Retrieves the data associated with the specified State.
     * @param {State} stateVariable The State data to retrieve.
     */
    static getStateData(stateVariable) {
        return eventStateData[state];
    }

    /**
     * Associates the specified State variable to the data.
     * @param {*} stateVariable The State variable to set the data for.
     * @param {*} data The data to set.
     */
    static setStateData(stateVariable, data) {
        eventStateData[stateVariable] = data;
    }

    /**
     * Subscribes the object to the specified list of Events.
     * @param {*} obj Required. The object to subscribe.
     * @param  {...any} args Required. A list of one or more Events to subscribe the object to.
     */
    static subscribe(obj = required("obj"), ...args) {
        if(args.length == 0)
            throw "objs cannot be null, and at least one arg must be specified";

        for(const eventName of args) {
            if(eventSubscription[eventName] != null && eventSubscription[eventName].find(o => o == obj) == null) {
                eventSubscription[eventName].push(obj);
            }
        }
    }

    /**
     * Unsubscribes the specified object from the Events in the args parameter, or all Events if this parameter is left empty.
     * @param {*} obj Required. The object to unsubscribe.
     * @param  {...any} args Optional. The Events to unsubscribe from. If this parameter is empty, the object is unsubscribed from all Events.
     */
    static unsubscribe(obj = required("obj"), ...args) {
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
            console.log(`Globally unsubscribed an object.`)
        }
    }

    /**
     * Invoke all event handlers passing in the associated event data.
     * @param {*} event Required. The Event to raise.
     * @param {*} data Optional. The data associated with the Event to raise.
     */
    static raiseEvent(event = required("event"), data) {
        for(const objToInvoke of eventSubscription[event]) {
            if(objToInvoke != null) {
                if(objToInvoke[event] != null) // for objects
                    objToInvoke[event](event, data);
                else if(typeof objToInvoke === "function") // for functions
                    objToInvoke(event, data);
            }
        }
    }
}

export { AppState, Events, State }
