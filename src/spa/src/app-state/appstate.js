import { AppState } from 'brainlet';

const GlobalState = new AppState();

/**
 * Represents the Events components can subscribe and unsubscribe from.
 */
const Events = {
  LOGIN: "onAppEventLogin",
  LOGOUT: "onAppEventLogout",
  NOTIFICATION: "onAppEventNotification"
};

/**
 * Represents all State variables that can have data associated with them.
 */
const State = {
  CURRENT_USER: "stateCurrentUser"
};

export { GlobalState, Events, State };
