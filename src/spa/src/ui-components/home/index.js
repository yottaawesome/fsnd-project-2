import { Component, linkEvent } from 'inferno';
import { AppState, Events, State } from '../../app-state'
import styles from './styles.module.scss'

export default class Home extends Component {
    constructor(props) {
        super(props);
        //this.componentDidMount = this.componentDidMount.bind(this);
    }

    componentDidMount() { }

    componentWillUnmount() { }

    onAppEventLogin(event, data) { }

    onLoginClick() {
        AppState.raiseEvent(Events.LOGIN, { name: 'Vasilios Magriplis' });
    }

    onLogoutClick() {
        AppState.setStateData(State.CURRENT_USER, null);
        AppState.raiseEvent(Events.LOGOUT, null);
    }

    render() {
        return (
            <div className={styles.red}>
                <h1>Hello</h1>
                <button onClick={linkEvent(this, this.onLoginClick)}>Login</button>
                <button onClick={linkEvent(this, this.onLogoutClick)}>Logout</button>
            </div>
        );
    }
}
