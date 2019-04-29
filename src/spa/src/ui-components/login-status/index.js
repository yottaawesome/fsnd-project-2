import { Component } from 'inferno';
import styles from './styles.module.scss';
import { GlobalState, Events } from '../../app-state';
import autobind from 'auto-bind';

export default class LoginStatus extends Component {
    constructor(props) {
        super(props);
        autobind(this);
        GlobalState.subscribe(this, Events.LOGIN, Events.LOGOUT);
        this.state = {
            user: null
        }
    }

    componentWillUnmount() { 
        GlobalState.unsubscribe(this);
    }

    onAppEventLogin(event, data) {
        this.setState({ user: data });
    }
    
    onAppEventLogout(event, data) {
        this.setState({ user: null });
    }

    render() {
        return (
            <div>
                {this.state.user == null ? 'You are not logged in' : `Hello, ${this.state.user.name}`  }
            </div>
        )
    }
}