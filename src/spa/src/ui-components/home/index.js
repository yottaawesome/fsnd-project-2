import { Component, linkEvent } from 'inferno';
import { GlobalState, Events, State } from '../../app-state'
import styles from './styles.module.scss'
import autobind from 'auto-bind';

export default class Home extends Component {
    constructor(props) {
        super(props);
        //this.componentDidMount = this.componentDidMount.bind(this);
        autobind(this);
        this.state = {}
        GlobalState.subscribe(this, Events.LOGIN);
    }

    componentDidMount() { 
        let currentUser = GlobalState.getStateData(State.CURRENT_USER);
        if(currentUser == null)
            this.setState({
                user: null
            });
        else {
            this.setState({
                user: currentUser
            });
        }
    }

    componentWillUnmount() { 
        GlobalState.unsubscribe(this);
    }

    onAppEventLogin(event, data) { 
        this.setState({
            user: data
        });
    }

    onLoginClick() {
        GlobalState.raiseEvent(Events.LOGIN, { name: 'Vasilios Magriplis' });
    }

    onLogoutClick() {
        GlobalState.setStateData(State.CURRENT_USER, null);
        GlobalState.raiseEvent(Events.LOGOUT, null);
    }

    render() {
        console.log(this.state.user);
        return (
            <div className={styles.red}>
                <h1>{this.state.user != null ? `Hello, ${this.state.user.name}!` : "Hello!"}</h1>
                <button onClick={linkEvent(this, this.onLoginClick)}>Login</button>
                <button onClick={linkEvent(this, this.onLogoutClick)}>Logout</button>
            </div>
        );
    }
}
